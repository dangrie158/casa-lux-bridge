import ctypes
from typing import Dict, List, Type

uint16_be = ctypes.c_uint16.__ctype_be__


class Register(ctypes.BigEndianStructure):
    length: int = 2
    address: int

    __known_registers: Dict[int, Type["Register"]] = {}

    def __init_subclass__(cls, *args, **kwargs) -> None:
        cls.__known_registers[cls.address] = cls
        super().__init_subclass__(*args, **kwargs)

    @classmethod
    def for_address(cls, address):
        return cls.__known_registers[address]

    def __repr__(self):
        values = [f"{name}={getattr(self, name)}" for name, _, _ in self.__class__._fields_ if name != "_"]
        return f"{self.__class__.__name__}({', '.join(values)})"

    def __format__(self, __format_spec: str) -> str:
        if __format_spec == "full":
            return f"{self!r}"
        elif __format_spec == "short":
            return f"{self.__class__.__name__}"
        return super().__format__(__format_spec)


class SynthLock(Register):
    address = 0x03
    _fields_ = (
        ("_", uint16_be, 3),
        ("RF_SYNTH_LOCK", uint16_be, 1),
        ("_", uint16_be, 12),
    )


class RSSI(Register):
    address = 0x06
    _fields_ = (
        ("RAW_RSSI", uint16_be, 6),
        ("_", uint16_be, 10),
    )


class RxTxConfig(Register):
    address = 0x07
    _fields_ = (
        ("_", uint16_be, 7),
        ("TX_EN", uint16_be, 1),
        ("RX_EN", uint16_be, 1),
        ("RF_PLL_CH_NO", uint16_be, 7),
    )


class PAConfig(Register):
    address = 0x09
    _fields_ = (
        ("PA_PWCTR", uint16_be, 4),
        ("_", uint16_be, 1),
        ("PA_GN", uint16_be, 4),
        ("_", uint16_be, 7),
    )


class XTALConfig(Register):
    address = 0x0A
    _fields_ = (
        ("_", uint16_be, 15),
        ("XTAL_OSC_EN", uint16_be, 1),
    )


class RSSIConfig(Register):
    address = 0x0B
    _fields_ = (
        ("_", uint16_be, 7),
        ("RSSI_PDN", uint16_be, 1),
        ("_", uint16_be, 8),
    )


class VCOConfig(Register):
    address = 0x17
    _fields_ = (
        ("_", uint16_be, 13),
        ("TxRx_VCO_CAL_EN", uint16_be, 1),
        ("_", uint16_be, 2),
    )


class XTALTrim(Register):
    address = 0x1B
    _fields_ = (
        ("_", uint16_be, 10),
        ("XI_trim", uint16_be, 6),
    )


class VersionInfo(Register):
    address = 0x1D
    _fields_ = (
        ("_", uint16_be, 8),
        ("RF_VER_ID", uint16_be, 4),
        ("_", uint16_be, 1),
        ("DIGITAL_VER_ID", uint16_be, 3),
    )


class IDCodeLower(Register):
    address = 0x1E
    _fields_ = (("ID_CODE_L", uint16_be, 16),)


class IDCodeUpper(Register):
    address = 0x1F
    _fields_ = (
        ("RF_CODE_ID", uint16_be, 4),
        ("ID_CODE_M", uint16_be, 12),
    )


class FormatConfig(Register):
    address = 0x20
    _fields_ = (
        ("PREAMBLE_LEN", uint16_be, 3),
        ("SYNCWORD_LEN", uint16_be, 2),
        ("TRAILER_LEN", uint16_be, 3),
        ("DATA_PACKET_TYPE", uint16_be, 2),
        ("FEC_TYPE", uint16_be, 2),
        ("BRCLK_SEL", uint16_be, 3),
        ("_", uint16_be, 1),
    )


class DelayConfig33(Register):
    length = 4
    address = 0x21
    _fields_ = (
        ("VCO_ON_DELAY_CNT", uint16_be, 8),
        ("TX_PA_OFF_DELAY", uint16_be, 2),
        ("TX_PA_ON_DELAY", uint16_be, 6),
    )


class DelayConfig34(Register):
    address = 0x22
    _fields_ = (
        ("BPKTCTL_DIRECT", uint16_be, 1),
        ("TX_CW_DLY", uint16_be, 7),
        ("_", uint16_be, 2),
        ("TX_SW_ON_DELAY", uint16_be, 6),
    )


class PowerConfig(Register):
    address = 0x23
    _fields_ = (
        ("POWER_DOWN", uint16_be, 1),
        ("SLEEP_MODE", uint16_be, 1),
        ("_", uint16_be, 1),
        ("BRCLK_ON_SLEEP", uint16_be, 1),
        ("TRANSMIT_TIMES", uint16_be, 4),
        ("MISO_TRI_OPT", uint16_be, 1),
        ("SCRAMBLE_DATA", uint16_be, 7),
    )


class SyncWord0(Register):
    address = 0x24
    _fields_ = (("SYNC_WORD", uint16_be, 16),)


class SyncWord1(Register):
    address = 0x25
    _fields_ = (("SYNC_WORD", uint16_be, 16),)


class SyncWord2(Register):
    address = 0x26
    _fields_ = (("SYNC_WORD", uint16_be, 16),)


class SyncWord3(Register):
    address = 0x27
    _fields_ = (("SYNC_WORD", uint16_be, 16),)


class FIFOThresholdConfig(Register):
    address = 0x28
    _fields_ = (
        ("FIFO_EMPTY_THRESHOLD", uint16_be, 5),
        ("FIFO_FULL_THRESHOLD", uint16_be, 5),
        ("SYNCWORD_THRESHOLD", uint16_be, 6),
    )


class FramerConfig(Register):
    address = 0x29
    _fields_ = (
        ("CRC_ON", uint16_be, 1),
        ("SCRAMBLE_ON", uint16_be, 1),
        ("PACK_LENGTH_EN", uint16_be, 1),
        ("FW_TERM_TX", uint16_be, 1),
        ("AUTO_ACK", uint16_be, 1),
        ("PKT_FIFO_POLARITY", uint16_be, 1),
        ("_", uint16_be, 2),
        ("CRC_INITIAL_DATA", uint16_be, 8),
    )


class RSSIScanConfig(Register):
    address = 0x2A
    _fields_ = (
        ("SCAN_RSSI_CH_NO", uint16_be, 6),
        ("_", uint16_be, 2),
        ("RX_ACK_TIME", uint16_be, 8),
    )


class RSSIScanControl(Register):
    address = 0x2B
    _fields_ = (
        ("SCAN_RSSI_EN", uint16_be, 1),
        ("SCAN_STRT_CH_OFFST", uint16_be, 7),
        ("WAIT_RSSI_SCAN_TIM", uint16_be, 8),
    )


class DatarateConfig(Register):
    address = 0x2C
    _fields_ = (
        ("DATARATE", uint16_be, 8),
        ("_", uint16_be, 8),
    )


class OptionConfig(Register):
    address = 0x2D
    _fields_ = (("OPTION", uint16_be, 16),)


class Flags(Register):
    address = 0x30
    _fields_ = (
        ("CRC_ERROR", uint16_be, 1),
        ("FEC23_ERROR", uint16_be, 1),
        ("FRAMER_ST", uint16_be, 6),
        ("SYNCWORD_RECV", uint16_be, 1),
        ("PKT_FLAG", uint16_be, 1),
        ("FIFO_FLAG", uint16_be, 1),
        ("_", uint16_be, 5),
    )


class FIFO(Register):
    address = 0x32
    _fields_ = (("TXRX_FIFO_REG", uint16_be, 16),)


class FIFOStatus(Register):
    address = 0x34
    _fields_ = (
        ("CLR_W_PTR", uint16_be, 1),
        ("_", uint16_be, 1),
        ("FIFO_WR_PTR", uint16_be, 6),
        ("CLR_R_PTR", uint16_be, 1),
        ("_", uint16_be, 1),
        ("FIFO_RD_PTR", uint16_be, 6),
    )


if __name__ == "__main__":
    reg = Register.for_address(0x2B).from_buffer(bytearray([0x80, 0x80]))
    print(reg)
