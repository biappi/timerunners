from dumper import *

FILENAME = "../original/GAME_DIR/AR1/FIL/LOGITAB.TAB"

tab_desc = (
    (array, 'offsets', {
        'items_struct': ( (uint16_be, 'off'), ),
        'items': fixed(0x4d),
    }),
    (uint16_be, 'stop_marker'),
    (block, 'items', {
        'offset': relative('.offsets.{i}.off'),
        'items_struct': (
            (run_until, 'items', {'end_byte': fixed(0xff)}),
        ),
        'count': fixed(0x4d),
    }),
)

dump_file(tab_desc, FILENAME)


