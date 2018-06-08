from dumper import *

FILENAME_USC = "../original/GAME_DIR/AR1/FIL/USC"
FILENAME_PRT = "../original/GAME_DIR/AR1/FIL/PRT"

usc_desc = (
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

dump_file(usc_desc, FILENAME_USC)
print
print
dump_file(usc_desc, FILENAME_PRT)


