from dumper import *

FILENAME = "../original/GAME_DIR/AR1/FIL/USC"

desc = (
    (array, 'exits', {
        'items_struct': (
            (uint8,     'room_from'),
            (uint8,     'room_to'),
            (uint16_be, 'from_y'),
            (uint16_be, 'to_y'),
        ),
        'items': fixed(30), # in reality they go on until the stop marker 0xffff
    }),
    (uint16_be, 'stop_marker'),
)

