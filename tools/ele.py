from dumper import *
from pal import load_palette
import sys
from bitmappe import Bitmappe

ele_desc = (
    (uint16, 'width'),
    (uint16, 'count'),
    (uint8,  'must_be_2'),
    (array,  'lines', {
        'items_struct': (
            (run_until, 'line', {'end_byte': fixed(0xff)}),
        ),
        'items': relative('count'),
    }),
    (uint16, 'stop_mark'),
)

ele_file = (
    (uint16, 'image_count'),
    (array,  'relocations', {
        'items_struct': (
            (uint16, 'off'),
            (uint16, 'seg'),
        ),
        'items': relative('image_count'),
    }),
    (block, 'eles', {
        'offset': add(relative('.relocations.{i}.off'), fixed(2)),
        'items_struct': ele_desc,
        'count': relative('image_count'),
    }),
)

def draw_ele(ele, col=1, p=None):
    class printer(object):
        def skip(self, n):
            sys.stdout.write('  ' * n)

        def put(self, n):
            if n == 0:
                sys.stdout.write('  ')
            else:
                sys.stdout.write('%02x' % n)

        def row(self):        
            sys.stdout.write('\n')

    if p is None: p =  printer()

    ele_content = reduce (lambda a, b: a + b, (l['line'] for l in ele['lines'])) + bytearray((0xff,0xff))
    the_ele = iter(ele_content)

    consecutive_ff = 0

    while True:
        skip = next(the_ele)

        if skip != 0xff:
            consecutive_ff = 0
            p.skip(skip)

            count = next(the_ele)

            if count != 0xff:
                consecutive_ff = 0

                for _ in xrange(count / 2):
                    colors = next(the_ele)
                    color1 = (colors & 0x0f)      + col
                    color2 = (colors & 0xf0 >> 4) + col

                    p.put(color1)
                    p.put(color2)

                if count & 1:
                    color = next(the_ele)
                    color1 = (color & 0x0f) + col
                    p.put(color1)
            else:
                consecutive_ff += 1
                if consecutive_ff == 3:
                    return
        else:
            p.row()

            consecutive_ff += 1
            if consecutive_ff == 3:
                return

def show_ele(ele, palette, col=1, mult=1, filename=None):
    import imageutils

    class imager(object):
        def __init__(self):
            self.width = ele['width']
            self.height = ele['count']
            self.image = imageutils.Image(self.width, self.height)
            self.curx = 0
            self.cury = 0

        def skip(self, n):
            for i in xrange(n):
                self.put(0)

        def put(self, n):
            self.image.put(self.curx,
                           self.cury,
                           n)
            self.curx += 1
            assert self.curx < self.width + 1
            # +1 because i assert after increment

        def row(self):        
            self.curx  = 0
            self.cury += 1

    i = imager()
    draw_ele(ele, col, i)

    if not filename:
        i.image.show(palette, mult)
    else:
        print [bytearray([i.image.get(a, b) for a in range(0, i.width)]) for b in range(0, i.height)][::-1]
        Bitmappe.to_file(
            [(int(r, 16), int(g, 16), int(b, 16)) for (r, g, b) in [(q[1:3], q[3:5], q[5:]) for q in palette]],
            [bytearray([i.image.get(a, b) for a in range(0, i.width)]) for b in range(0, i.height)], i.width, i.height,
            filename
        )
        #i.image.save_image(palette, mult, filename)

if __name__ == '__main__':
    FILENAME = '../original/GAME_DIR/AR1/IMG/K.ELE'
    FILENAME = '../original/GAME_DIR/AR1/UCC/UCCI0.ELE'
    FILENAME = '../original/GAME_DIR/AR1/IMG/TR.ELE'

    x = parse_file(ele_file, FILENAME)

    pal_file = "../original/GAME_DIR/AR1/STA/ARCADE.PAL"
    palette = load_palette(pal_file)

    for i, e in enumerate(x['eles']):
        print i
        show_ele(e, palette, -63, 1, filename='%d.gif' % i)
