#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2018 jem@seethis.link
# Licensed under the MIT license (http://opensource.org/licenses/MIT)

from __future__ import absolute_import, division, print_function, unicode_literals

from keyplus.keycodes import *

class LayoutDeviceKeycodes(object):
    def __init__(self, keycodes=None, number_keys=None, keycode_mapper=None):
        if keycodes != None:
            self.keycodes = keycodes
        elif number_keys != None:
            self.keycodes = ['none'] * number_keys
        else:
            self.keycodes = []

    @property
    def number_keys(self):
        return len(self.keycodes)

    def to_json(self):
        result = []
        for keycode in self.keycodes:
            result.append(keycode)
        return result

    def to_keycodes(self, keycode_mapper):
        result = []
        for keycode in self.keycodes:
            result.append(keycode_mapper.from_string(keycode))
        return result


class LayoutLayer(object):
    def __init__(self, device_list=None, device_sizes=None):
        self.device_list = []
        if device_list != None:
            self.device_list = device_list
        elif device_sizes != None:
            for dev_size in device_sizes:
                self.device_list.append( LayoutDeviceKeycodes(number_keys = dev_size) )

    @property
    def number_devices(self):
        return len(self.device_list)

    def add_device_layer(self, device_layer):
        self.device_list.append(device_layer)

    def to_json(self):
        result = []
        for device in self.device_list:
            result.append(device.to_json())
        return result

    def to_keycodes(self, keycode_mapper):
        result = []
        for device in self.device_list:
            result.append(device.to_keycodes(keycode_mapper))
        return result


class LayoutKeyboard(object):
    def __init__(self, layout_id, number_layers=0, device_sizes=None):
        """
        Args:
            layout_id: can be a string or an integer.
        """
        self.layout_id = layout_id
        self.default_layer = 0
        self.layer_list = []
        if device_sizes != None:
            self.device_sizes = device_sizes
        else:
            self.device_sizes = [0]
        for _ in range(number_layers):
            self.layer_list.append(LayoutLayer(device_sizes = device_sizes))

        self.set_keycode_mapper(KeycodeMapper())

    @property
    def number_layers(self):
        return len(self.layer_list)

    def set_keycode(self, layer, device, key_number, keycode):
        self.layer_list[layer].device_list[device].keycodes[key_number] = keycode

    def to_json(self):
        result = {}

        result['default_layer'] = self.default_layer

        layers = []
        for layer in self.layer_list:
            layers.append(layer.to_json())
        result['layers'] = layers

        return result

    def parse_json(self, layout_id, parser_info=None):
        if parser_info == None:
            parser_info = KeyplusParserInfo(
                "<LayoutKeyboard>",
                {layout_id: layout_json},
                print_warnings = True
            )
        parser_info.enter(layout_id)
        self.default_layer = parser_info.try_get(
            field = 'default_layer',
            field_type = int,
            default = 0,
        )
        parser_info.exit()

    def set_keycode_mapper(self, keycode_mapper):
        self.keycode_mapper = keycode_mapper

    def load_keycodes(self, keycodes):
        self.layer_list = []
        for layer in keycodes:
            layer_obj = LayoutLayer()
            self.layer_list.append(layer_obj)
            for device in layer:
                device_obj = LayoutDeviceKeycodes()
                self.layer_list[-1].add_device_layer(device_obj)
                for keycode in device:
                    keycode_name = self.keycode_mapper.keycode_to_string(keycode)
                    device_obj.keycodes.append(keycode_name)

    def to_keycodes(self):
        result = []
        for layer in self.layer_list:
            result.append(layer.to_keycodes(self.keycode_mapper))
        return result


"""
layouts:
  split_layout:
    default_layer: 0
    layers: [
      [ # layer 0 (colemak)
        [ # left hand
          tab , q   , w   , f   , p   , g   ,
          ent , a   , r   , s   , t   , d   ,
          lalt, z   , x   , c   , v   , b   ,
          esc , L6  , lctl, spc , L5  ,
        ],
        [ # right hand
          j   , l   , u   , y   , ";" , "-" ,
          h   , n   , e   , i   , o   , "'" ,
          k   , m   , "," , "." , "/" , "`" ,
          bspc, sticky_lshift, sticky_L4, lgui, esc ,
        ],
      ],
      [ # layer 1 (dvorak)
        [ # left hand
          ____, "'" , "," , "." , p   , y   ,
          ____, a   , o   , e   , u   , i   ,
          ____, ";" , q   , j   , k   , x   ,
          ____, ____, ____, ____, ____,
        ],
        [ # right hand
          f   , g   , c   , r   , l   , "/" ,
          d   , h   , t   , n   , s   , "-" ,
          b   , m   , w   , v   , z   , "`" ,
          ____, ____, ____, ____, ____,
        ],
      ],
      [ # layer 2 (qwerty)
        [ # left hand
          ____, q   , w   , e   , r   , t   ,
          ____, a   , s   , d   , f   , g   ,
          ____, z   , x   , c   , v   , b   ,
          ____, ____, ____, ____, ____,
        ],
        [ # right hand
          y   , u   , i   , o   , p   , "-" ,
          h   , j   , k   , l   , ";" , "'" ,
          m   , n   , "," , "." , "/" , "`" ,
          ____, ____, ____, ____, ____,
        ],
      ],
      [ # layer 6 (qwerty arrows)
        [ # left hand
          ____, q   , w   , e   , r   , t   ,
          ____, a   , s   , d   , f   , g   ,
          ____, z   , x   , c   , v   , b   ,
          ____, ____, ____, ____, ____,
        ],
        [ # right hand
          y   , u   , up  , o   , p   , "-" ,
          h   , left, down, rght, ";" , "'" ,
          m   , n   , "," , "." , "/" , "`" ,
          ____, ____, ____, ____, ____,
        ],
      ],
      [ # layer 3 (symbol)
        [ # left hand
          ____, "|" , "2" , "3" , "4" , "5" ,
          ____, "1" , "\\", "(" , "[" , "{" ,
          ____, "!" , "@" , "#" , "$" , "%" ,
          ____, ____, ____, ____, ____,
        ],
        [ # right hand
          "6" , "7" , "8" , "9" , "+" , "-" ,
          "}" , "]" , ")" , "=" , "0" , "*" ,
          "^" , "&" , "," , "." , "/" , "~" ,
          ____, ____, ____, ____, ____,
        ],
      ],
      [ # layer 4 (fn)
        [ # left hand
          ins , del , home, up  , end , pgup,
          ____, esc , left, down, rght, pgdn,
          ____, F1  , F2  , F3  , F4  , F5  ,
          ____, ____, ____, ____, ____,
        ],
        [ # right hand
          C-pgup, C-home, C-up  , C-end , C-del , F12 ,
          C-pgdn, C-left, C-down, C-rght, C-bspc, F11 ,
          F6    , F7    , F8    , F9    , F10   , CA-none ,
          ____  , ____  , ____  , ____  , ____  ,
        ],
      ],
      [ # layer 5 (media)
        [ # left hand
          slck, pscr, mply, volu, mstp, F11 ,
          bspc, mute, mprv, vold, mnxt, app ,
          ____, C-y , CS-z , C-i , C-. , C-; ,
          ____, ____, ____, ____, ____,
        ],
        [ # right hand
          wh_u, btn1, ms_u, btn2, RS-c, dongle_0 ,
          wh_d, ms_l, ms_d, ms_r, btn3, dongle_1 ,
          set_l3 , set_l0 , set_l1 , set_l2 , NONE, pair ,
          ____, ____, ____, ____, ____,
        ],
      ],
    ]
  numpad_layout:
    default_layer: 0
    layers: [
      [ # layer 0
        # [ # numpad (no matrix_map)
        #   nlck, kp_/, kp_*, kp_-  ,
        #   kp_7, kp_8, kp_9, kp_a  ,
        #   kp_4, kp_5, kp_6, none  ,
        #   kp_1, kp_2, kp_3, kp_ent,
        #   kp_0, none, kp_., none  ,
        # ]
        [ # numpad (with matrix_map)
          nlck, kp_/, kp_*, kp_-  ,
          kp_7, kp_8, kp_9, kp_a  ,
          kp_4, kp_5, kp_6,
          kp_1, kp_2, kp_3, kp_ent,
          kp_0,       kp_.
        ]
      ]
    ]
  gamma_split:
    default_layer: 0
    layers: [
      [ # layer 0 (colemak)
        [ # left hand
          tab , q   , w   , f   , p   , g   ,
          SFTEnt , a   , r   , s   , t   , d   ,
          lalt, z   , x   , c   , v   , b   ,
          esc , L4  , L4  , lctl  , L3  , spc ,
        ],
        [ # right hand
          j   , l   , u   , y   , ";" , "-" ,
          h   , n   , e   , i   , o   , "'" ,
          k   , m   , "," , "." , "/" , "`" ,
          sticky_lshift, sticky_L2, bspc, lgui, esc , ralt
        ],
      ],
      [ # layer 1 (qwerty arrows)
        [ # left hand
          ____, q   , w   , e   , r   , t   ,
          ____, a   , s   , d   , f   , g   ,
          ____, z   , x   , c   , v   , b   ,
          ____, ____, ____, ____, ____, ____,
        ],
        [ # right hand
          y   , u   , up  , o   , p   , "-" ,
          h   , left, down, rght, ";" , "'" ,
          m   , n   , "," , "." , "/" , "`" ,
          ____, ____, ____, ____, ____, ____,
        ],
      ],
      [ # layer 2 (symbol)
        [ # left hand
          ____, "|" , "2" , "3" , "4" , "5" ,
          ____, "1" , "\\", "(" , "[" , "{" ,
          ____, "!" , "@" , "#" , "$" , "%" ,
          ____, ____, ____, ____, ____, ____,
        ],
        [ # right hand
          "6" , "7" , "8" , "9" , "+" , "-" ,
          "}" , "]" , ")" , "=" , "0" , "*" ,
          "^" , "&" , "," , "." , "/" , "~" ,
          ____, ____, ____, ____, ____, ____,
        ],
      ],
      [ # layer 3 (fn)
        [ # left hand
          ins , del , home, up  , end , pgup,
          ____, esc , left, down, rght, pgdn,
          ____, F1  , F2  , F3  , F4  , F5  ,
          ____, ____, ____, ____, ____, ____,
        ],
        [ # right hand
          C-pgup, C-home, C-up  , C-end , C-del , F12 ,
          C-pgdn, C-left, C-down, C-rght, C-bspc, F11 ,
          F6    , F7    , F8    , F9    , F10   , CA-none ,
          ____  , ____  , ____  , ____  , ____  , ____,
        ],
      ],
      [ # layer 4 (media)
        [ # left hand
          slck, pscr, mply, volu, mstp, F11 ,
          bspc, mute, mprv, vold, mnxt, app ,
          ____, C-y , CS-z , C-i , C-. , C-; ,
          ____, ____, ____, ____, ____, ____,
        ],
        [ # right hand
          wh_u, btn1, ms_u, btn2, RS-c, dongle_0 ,
          wh_d, ms_l, ms_d, ms_r, btn3, dongle_1 ,
          set_l3 , set_l0 , set_l1 , set_l2 , NONE, test_2 ,
          ____, ____, ____, ____, ____, ____,
        ],
      ],
    ]
"""
