from dumper import *

FILENAME = "../original/GAME_DIR/AR1/FIL/USC"
FILENAME = "../original/GAME_DIR/AR1/FIL/PRT"

desc = (
    (array, 'exits', {
        'items_struct': (
            (uint8,     'room_to'),
            (uint8,     'room_from'),
            (uint16_be, 'from_y'),
            (uint16_be, 'to_y'),
            (uint16_be, 'unk1'),
            (uint16_be, 'unk2'),
        ),
        'items': fixed(58), # in reality they go on until the stop marker 0xffff
    }),
    (uint16_be, 'stop_marker'),
)

