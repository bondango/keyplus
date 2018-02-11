#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2018 jem@seethis.link
# Licensed under the MIT license (http://opensource.org/licenses/MIT)

import io_map.chip_id

from io_map.common import IoMapper, IoMapperError, IoMapperPins


XmegaPinsA4U = IoMapperPins(
    ports = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'R': 5
    },
    pins = [
        0xff,
        0x0f,
        0xff,
        0x3f,
        0x0f,
        0x03,
    ],
    port_size = 8
)

XmegaPinsA3U = IoMapperPins(
    ports = None,
    pins = None,
    port_size = 8
)

XmegaPinsA1U = IoMapperPins(
    ports = None,
    pins = None,
    port_size = 8
)

class IoMapperXmega(IoMapper):
    XMEGA_SERIES_TABLE = {
        'A4U': XmegaPinsA4U,
        'A3U': XmegaPinsA3U,
        'C3': XmegaPinsA3U, # same as A series
        'A1U': XmegaPinsA1U,
        'C1': XmegaPinsA1U, # same as A series
    }

    def __init__(self, chip_id):
        self.chip_info = io_map.chip_id.lookup_chip_id(chip_id)

        assert(self.chip_info != None)
        assert(self.chip_info.architecture == 'XMEGA')
        assert(self.chip_info.series in self.XMEGA_SERIES_TABLE)

    def get_pin_number(self, pin_name):
        try:
            pin_name = pin_name.upper()
            port = pin_name[0]
            pin = int(pin_name[1:])
        except:
            raise IoMapperError("Invalid pin name '{}', correct format "
                                "is a letter followed by a number. E.g. C1, B0, etc"
                                .format(pin_name))

        pin_map = IoMapperXmega.XMEGA_SERIES_TABLE[self.chip_info.series]

        if not pin_map.is_valid_pin(port, pin):
            raise IoMapperError("The pin '{}' does not exist on the given microcontroller '{}'"
                                .format(pin_name, self.chip_info.name))

        return pin_map.get_pin_number(port, pin)