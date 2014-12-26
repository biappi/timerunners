from dumper import *
import sys

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

