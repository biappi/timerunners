from dumper import *
from ele import ele_desc, show_ele, draw_ele
from pal import load_palette
from imageutils import Image

FILENAME = "../original/GAME_DIR/PLR/BNK/ANIS09.ANI"

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
        'offset': add(relative('.palette_offset'), fixed(18)),
        'items_struct': (
            (array,  'colors', {
                'items_struct': {
                    (uint8, 'b'),
                    (uint8, 'g'),
                    (uint8, 'r'),
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


if 1:
    ani_file = parse_file(ani_desc, FILENAME)

    pal = ['#000000'] * 256

    def color_dict_to_string(c):
        return "#%02x%02x%02x" % (c['r'] << 2, c['g'] << 2, c['b'] << 2)

    for i, color in  enumerate(ani_file['palette'][0]['colors']):
        pal[i] = color_dict_to_string(color)

    def draw_frame(i):
        ele1 = ani_file['frames'][0]
        width, height = ele1['width'] + 3, ele1['count']
        img = Image(width, height)

        for y, l in enumerate(ele1['lines']):
            line = l['line'][2:-1]

            for x, c in enumerate(line):
                try:
                    img.put(x, y, c)
                except:
                    print "bad line", x, y, c

        img.show(pal, 2)
   
    for i in xrange(ani_file['count']):
        draw_frame(i)

else:
    dump_file(ani_desc, FILENAME)
