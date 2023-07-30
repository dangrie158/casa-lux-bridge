##
# This file is part of the libsigrokdecode project.
##
# Copyright (C) 2014 Jens Steinhauser <jens.steinhauser@gmail.com>
##
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
##
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
##
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
##

import enum
import typing

import sigrokdecode as srd

from .registers import *


class Annotation(typing.NamedTuple):
    id: int
    code: str
    display_name: str


class Annotations(enum.Enum):
    FIFO_DATA = Annotation(0, "fifo", "Payload")
    REG_WRITE = Annotation(1, "write", "Write")
    REG_READ = Annotation(2, "read", "Read")
    TRANSMISSION = Annotation(3, "tx", "Transmission")
    WARNING = Annotation(4, "warning", "Warning")


class Decoder(srd.Decoder):
    api_version = 3
    id = "lt8920"
    name = "LT8920"
    longname = "LT8920"
    desc = "Long range 2.4GHz Radio Transceiver"
    license = "gplv2+"
    inputs = ["spi"]
    outputs = []
    tags = ["IC", "Wireless/RF"]
    options = ()
    annotations = tuple(annotation.value[1:] for annotation in Annotations)
    annotation_rows = (
        ("commands", "Commands", (Annotations.REG_WRITE.value.id, Annotations.FIFO_DATA.value.id)),
        ("transmissions", "Transmissions", (Annotations.TRANSMISSION.value.id,)),
        ("responses", "Responses", (Annotations.REG_READ.value.id,)),
        ("warnings", "Warnings", (Annotations.WARNING.value.id,)),
    )

    def __init__(self):
        self.reset()

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

        self.reset()

    def reset(self):
        self.fifo = []
        self.fifo_pointer = 0

    def decode(self, start_sample, end_sample, data):
        packet_type, tx_payload, rx_payload = data
        if packet_type != "TRANSFER":
            return

        if len(tx_payload) < 2:
            self.put(
                start_sample, end_sample, self.out_ann, [Annotations.WARNING.value.id, [f"Incomplete Transfer", "INC"]]
            )
            return

        register_address, *tx_payload_data = tx_payload
        _, *rx_payload_data = tx_payload
        tx_payload_bytes = bytearray([data.val for data in tx_payload_data])
        rx_payload_bytes = bytearray([data.val for data in rx_payload_data])
        is_write = not bool(register_address.val & 0x80)
        address = register_address.val & 0x7F

        try:
            write_reg = Register.for_address(address).from_buffer(tx_payload_bytes)
            read_reg = Register.for_address(address).from_buffer(rx_payload_bytes)
        except KeyError:
            self.put(
                register_address.ss,
                register_address.es,
                self.out_ann,
                [Annotations.WARNING.value.id, [f"Unknown Register Adress: {address:02X}", "UNK"]],
            )
            return

        operation = "write" if is_write else "read"
        if is_write:
            tx_message = f"{operation} {write_reg:full}"
            self.put(start_sample, end_sample, self.out_ann, [Annotations.REG_WRITE.value.id, [tx_message]])
        else:
            tx_message = f"{operation} {write_reg:short}"
            rx_message = f"{read_reg:full}"

            self.put(
                register_address.ss, register_address.es, self.out_ann, [Annotations.REG_WRITE.value.id, [tx_message]]
            )
            self.put(
                rx_payload_data[0].ss,
                rx_payload_data[-1].es,
                self.out_ann,
                [Annotations.REG_READ.value.id, [rx_message]],
            )

        # update the simple FIFO statemachine
        if address == FIFO.address and is_write:
            for byte in tx_payload_bytes:
                self.fifo.insert(self.fifo_pointer, byte)
                self.fifo_pointer += 1
        elif address == RxTxConfig.address and is_write and write_reg.TX_EN == 1:
            fifo_repr = " ".join([f"{byte:02X}" for byte in self.fifo])

            self.put(
                end_sample,
                end_sample + 10 * len(fifo_repr),
                self.out_ann,
                [Annotations.TRANSMISSION.value.id, [fifo_repr]],
            )
        elif address == FIFOStatus.address and is_write and write_reg.CLR_W_PTR == 1:
            self.fifo_pointer = 0
            self.fifo.clear()
