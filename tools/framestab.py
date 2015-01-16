from dumper import *

FILENAME = "../original/GAME_DIR/AR1/FIL/FRAMES.TAB"

tab_desc = (
    (array, 'offsets', {
        'items_struct': (
            (uint16_be, 'off'),
        ),
        'items': fixed(106),
    }),
    (block, 'anims', {
        'offset': relative('.offsets.{i}.off'),
        'count': fixed(106),
        'items_struct': (
            (array, 'frames', {
                'items_struct': ( 
                    (uint8, 'time'),
                    (uint8, 'frame'),
                    (stop_if, '', {
                        'is_zero': add(relative('time'), relative('frame')),
                    }),
                    (uint8, 'x_delta'),
                    (uint8, 'y_delta'),
                    (uint8, 'flip'),
                ),
            }),
        ),
    }),
)

dump_file(tab_desc, FILENAME)


