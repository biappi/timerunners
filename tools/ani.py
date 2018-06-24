from dumper import *
from ele import ele_desc
from imageutils import Image
import sys

FILENAME = "../original/GAME_DIR/PLR/BNK/ANIX05.ANI"

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
        'items_struct': ele_desc,
        'count': add(relative('.count'), fixed(-1)),
    }),
)


def color_dict_to_string(c):
    return "#%02x%02x%02x" % (c['b'] << 2, c['g'] << 2, c['r'] << 2)

def draw_ani_ele(ele):
    def line_expand_ani(l):
        q = iter(l[:-1])
        r = []
        while True:
            try:
                r += [0] * next(q)
                count = next(q)
                for _ in xrange(count):
                    r.append(next(q))
            except StopIteration:
                return r

    width, height = ele['width'], ele['count']
    img = Image(width, height)

    for y, l in enumerate(ele['lines']):
        line = line_expand_ani(l['line'])
        for x, c in enumerate(line):
            try:
                img.put(x, y, c)
            except:
                print "bad line", x, y, c

    return img


try:
    x = parse_file(ani_desc, sys.argv[1])
except:
    x = parse_file(ani_desc, FILENAME)

pal = map(color_dict_to_string, x['palette'][0]['colors'])

for ele in x['frames']:
    img = draw_ani_ele(ele)
    img.show(pal, 2)
