from dumper import *
import ele

FILENAME = "../original/GAME_DIR/PLR/BNK/ANIX05.ANI"

desc = (
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
        'items': add(relative('count'), fixed(-1)),
    }),

    (uint32, '00 ff 00 00'),
    (uint8, '08'),
    (block, 'palette', {
        'offset': add(relative('.palette_offset'), fixed(15)),
        'items_struct': (
            (array,  'colors', {
                'items_struct': {
                    (uint8, 'b'),
                    (uint8, 'g'),
                    (uint8, 'r'),
                },
                'items': fixed(256),
            }),
        ),
        'count': fixed(1)
    }),

    (block, 'frames', {
        'offset': add(relative('.items.{i}.boh'), fixed(10)),
        'items_struct': ele.ele_item,
        'count': add(relative('.count'), fixed(-1)),
    }),
)
