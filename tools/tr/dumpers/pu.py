from dumper import *

FILENAME = "../original/GAME_DIR/AR1/FIL/PU"

pu_item = (

    (uint16_be, 'x1'),
    (uint16_be, 'y1'),
    (uint16_be, 'x2'),
    (uint16_be, 'y2'),

    (uint8, 'ignored'),
    (uint8, 'ignored_set_zero'),
    (uint8, 'vita'), # vita = ($1 << 3) / 5
    (uint8, 'ignored'),

    (uint16, 'boh1'),

    (uint8, 'bool'),

    (uint8, 'maybe_item_type'),

    (uint16, 'ignored_copy_of_x1'),
    (uint16, 'ignored_copy_of_y1'),

    (uint8, 'sprite_nr'),
    (uint8, 'ignored'),
    (uint8, 'ignored'),
    (uint8, 'ignored'),

    (uint16_be, 'wanted_ucci_nr'),
    (uint16_be, 'unk27'),
)

desc = (
    (array, 'rooms', {
        'items_struct': (
            (array, 'pu', {
                'items_struct': pu_item,
                'items': fixed(2),
            }),
        ),
        'items': fixed(140/2),
   }),
)


