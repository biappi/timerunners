from dumper import *
import ele

FILENAME = "../original/GAME_DIR/PLR/WDW/PMOUSE.I16"

desc = (
    (uint16,  'offset_1st_element'),
    (uint16,  'offset_2st_element'),
    (uint16,  'offset_palette'),
    (block,   'first_ele', {
        'offset': relative('.offset_1st_element'),
        'items_struct': ele.ele_item,
        'count': fixed(1),
    }),
    (block,   'second_ele', {
        'offset': relative('.offset_2st_element'),
        'items_struct': ele.ele_item,
        'count': fixed(1),
    }),
    (block,   'palette', {
        'offset': relative('.offset_palette'),
        'items_struct': (
            (uint8,  'first_color'),
            (uint8,  'last_color'),
            (uint32, 'unused'),
            (array,  'colors', {
                'items_struct': (
                    (uint8, 'g'),
                    (uint8, 'b'),
                    (uint8, 'r'),
                ),
                'items_including': subtract(
                    relative('.palette.0.last_color'),
                    relative('.palette.0.first_color'),
                ),
            }),
        ),
        'count': fixed(1),
    }),
)
