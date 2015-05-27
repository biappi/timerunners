from dumper import *
from pal import load_palette, pal_desc
import sys
from palette import Palette
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

    data = [line_expand_ele(l['line'], ele['width']) for l in ele['lines']]
    for d in data:
        for q in d:
            p.put(q)
        p.row()

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
            self.image.put(self.curx, self.cury, n)
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


def line_expand_ele(line, w):
    q = iter(line[:-1])
    r = []
    c = 0xc1
    while True:
        try:
            r += [0] * next(q)
            count = next(q)
            for _ in xrange(count / 2):
                colors = next(q)
                r.append((colors & 0x0f) + c)
                r.append(((colors & 0xf0) >> 4) + c)
            if count & 1:
                r.append((next(q) & 0x0f) + c)
        except StopIteration:
            r += [0] * (w - len(r))
            #print ['%02x' % l for l in r]
            return r


def bittemappe_ele(ele_item, pal_path, output_bmp):
    palette = Palette.rgb_format_pal(parse_file(pal_desc, pal_path)['palette'])
    bmp_data = [line_expand_ele(l['line'], ele_item['width']) for l in ele_item['lines']]
    Bitmappe.to_file(palette, bmp_data, ele_item['width'], ele_item['count'], output_bmp)

if __name__ == '__main__':
    FILENAME = '../original/GAME_DIR/AR1/IMG/K.ELE'
    FILENAME = '../original/GAME_DIR/AR1/UCC/UCCI0.ELE'
    FILENAME = '../original/GAME_DIR/AR1/IMG/TR.ELE'

    x = parse_file(ele_file, FILENAME)

    pal_file = "../original/GAME_DIR/AR1/STA/ARCADE.PAL"
    palette = load_palette(pal_file)

    for i, e in enumerate(x['eles']):
        print i
        bittemappe_ele(e, pal_file, '%d.bmp' % i)
        show_ele(e, palette, -63, 1, filename='%d.gif' % i)
