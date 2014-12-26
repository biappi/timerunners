from dumper import *
from ele import ele_desc, draw_ele

FILENAME = "../original/GAME_DIR/PLR/WDW/PMOUSE.I16"
i16_desc = (
    (uint16,  'offset_1st_element'),
    (uint16,  'offset_2st_element'),
    (uint16,  'offset_palette'),
    (block,   'first_ele', {
        'offset': relative('.offset_1st_element'),
        'items_struct': ele_desc,
        'count': fixed(1),
    }),
    (block,   'second_ele', {
        'offset': relative('.offset_2st_element'),
        'items_struct': ele_desc,
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
                    (uint8, 'r'),
                    (uint8, 'g'),
                    (uint8, 'b'),
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

dump_file(i16_desc, FILENAME)
i16_file = parse_file(i16_desc, FILENAME)

print
draw_ele(i16_file['first_ele'][0])

print
draw_ele(i16_file['second_ele'][0])

