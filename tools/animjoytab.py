from dumper import *

FILENAME = "../original/GAME_DIR/AR1/FIL/ANIMJOY.TAB"

tab_desc = (
    (array, 'offsets', {
        'items_struct': (
            (array, 'offsets', {
                'items_struct': (
                    (uint8, 'i'),
                ),
                'items': fixed(18),
            }),
        ),
        'items': fixed(106),
    }),
)

dump_file(tab_desc, FILENAME)


