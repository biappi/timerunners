from dumper import *

FILENAME = "../original/GAME_DIR/AR1/FIL/PN"

desc = (
    (array, 'stars', {
        'items_struct': (
            (uint16_be, 'room_nr'),
            (uint16_be, 'score'),
            (uint16_be, 'y'),
            (uint16_be, 'x'),
        ),
        'items': fixed(22), # in reality they go on until the stop marker 0xffff
    }),
    (uint16_be, 'stop_marker'),
)

