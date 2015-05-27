from dumper import *
from ele import ele_desc, show_ele, draw_ele
from pal import load_palette

FILENAME = "../original/GAME_DIR/PLR/BNK/ANIX01.ANI"

ani_desc = (
    (uint16,   'unused1'),
    (uint16,   'count'),
    (uint16,   'size_in_memory'),
    (uint16,   'unused2'),
    (uint16,   'unused3'),

    (uint32,   'palette_offset'),

    (array,    'items', {
        'items_struct': {
            (uint32, 'boh'),
        },
        'items': relative('count'),
    }),

    (block, 'palette', {
        'offset': add(relative('.palette_offset'), fixed(10)),
        'items_struct': (
            (array,  'colors', {
                'items_struct': {
                    (uint8, 'r'),
                    (uint8, 'g'),
                    (uint8, 'b'),
                },
                'items': fixed(255),
            }),
        ),
        'count': fixed(1)
    }),

    (block, 'frames', {
        'offset': add(relative('.items.{i}.boh'), fixed(10)),
        'items_struct': ele_desc,
        'count': add(relative('.count'), fixed(-1)),
    }),
)

if 0:
    pal_file = "../original/GAME_DIR/AR1/STA/ARCADE.PAL"
    palette = load_palette(pal_file)

    x = parse_file(ani_desc, FILENAME)
    ele1 = x['frames'][0]
    draw_ele(ele1, 0)

else:
    dump_file(ani_desc, FILENAME)
