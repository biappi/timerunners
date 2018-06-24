from dumper import *

FILENAME = "../original/GAME_DIR/AR1/FIL/INI"

tab_desc = (
    (uint16_be, 'boh1'),
    (uint16_be, 'boh2'),
    (uint32_be, 'boh3'),
    (uint16_be, 'pupo_palette_delta'),
    (uint16_be, 'current_room_nr'),
    (uint16_be, 'pupo_x'),
    (uint16_be, 'pupo_y'),
    (uint16_be, 'colpi'),
    (uint16_be, 'counter_to_set_vita'),
)

'''

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
                    (uint8, 'frame'),
                    (uint8, 'time'),
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

'''

dump_file(tab_desc, FILENAME)


