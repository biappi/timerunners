from tr import dumpers

from pal import load_palette
from ..utils import imageutils

import sys

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
        i.image.save_image(palette, mult, filename)

def main(*args):
    FILENAME = '../original/GAME_DIR/AR1/IMG/K.ELE'
    FILENAME = '../original/GAME_DIR/AR1/UCC/UCCI0.ELE'
    FILENAME = '../original/GAME_DIR/AR1/IMG/TR.ELE'

    x = dumpers.parse_file(dumpers.ele.desc, FILENAME)

    pal_file = "../original/GAME_DIR/AR1/STA/ARCADE.PAL"
    palette = load_palette(pal_file)

    for i, e in enumerate(x['eles']):
        print i
        show_ele(e, palette, -63, 1, filename='%d.gif' % i)
