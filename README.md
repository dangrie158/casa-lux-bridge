# CasaLux LED Panel Broidge to WiFi

# What?
A WIP project to build a bridge for including CasaLux branded LED Panels that were sold by ALDI Süd (Germany) some time around 2021 ([Example](https://www.aldi-sued.de/de/p.casalux-led-panel.490000000000809780.html)) into Homeassistant.

# Why?
Because they hang everywhere in the house I rent and I don't want to modify anything about the hardware but still be able to remotely control them.

# How?
It seems like the units use a 2.4GHz Remote that works very close to the Milight Protocol that was already [reverse engineered](https://arduino-projects4u.com/milight-rf-control/), however they use another IC for the RF transmission.

The silkscreen on the chip is etched off, however it seems to be a [LT89XX](https://datasheet4u.com/datasheet-pdf/NST/LT8920/pdf.php?id=1404584) by NST Tech. The chip is pretty confidently identified by the initialisation sequence that basically matches the datasheet reccommendations bit-by-bit for all of the 20-or-so registers.

# State

| Step                             | Progress  | Note                                                                                                      |
|----------------------------------|-----------|-----------------------------------------------------------------------------------------------------------|
| Reverse Engineering the Hardware | **100 %** |                                                                                                           |
| Reverse Engineering the Protocol | **90 %**  | POC is missing                                                                                            |
| Library for ESP8266 / ESP32      | **0%**    |                                                                                                           |
| Hardware for Bridge              | **0%**    |                                                                                                           |
| Firmware for Bridge              | **0%**    | Maybe the [exitsing hub project](https://github.com/sidoh/esp8266_milight_hub/tree/master) can be adapted |
| Home Assistant integration       | **0%**    | Should not be necessary if the milight hub can be adapted                                                 |
