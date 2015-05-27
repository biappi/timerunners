from dumper import *
from ele import ele_desc, show_ele, draw_ele, line_expand_ele
from imageutils import Image
from palette import Palette

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

if 1:
    x = parse_file(ani_desc, FILENAME)
    print x

    pal = Palette.html_format_pal(x['palette'][0]['colors'])

    ele1 = x['frames'][0]
    width, height = ele1['width'], ele1['count']
    img = Image(width, height)

    print 'w, h:', width, height

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

    for y, l in enumerate(ele1['lines']):
        line = line_expand_ani(l['line'])
        for x, c in enumerate(line):
            try:
                img.put(x, y, c)
            except:
                print "bad line", x, y, c

    img.show(pal, 2)
    
else:
    dump_file(ani_desc, FILENAME)
