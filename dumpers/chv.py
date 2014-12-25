from dumper import *
import sys

FILENAME = "../original/GAME_DIR/FNT/MANAGER.CHV"

chv_desc = (
    (uint8, 'first_char'),
    (uint8, 'last_char'),
    (uint8, 'glyphs_format'), # 1 = ELE
    (uint8, 'space_width'),
    (uint8, 'must_be_7f'),
    (array, 'relocations', {
        'items_struct': (
            (uint16, 'offset'),
            (uint16, 'unk2'),
        ),
        'items_including': subtract(relative('.last_char'), relative('.first_char')),
    }),
    (block, 'glyphs', {
        'offset': add(relative('.relocations.{i}.offset'), fixed(5)), # this skips the global file header
        'items_struct': (
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
        ),
        'count_including': subtract(relative('.last_char'), relative('.first_char')),
        'ignore_if_FFFF': relative('.relocations.{i}.offset'),
    }),
)


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

def draw_ele(ele_content, col=1, p=printer()):
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

if __name__ == '__main__':
    def ele_content_from_dict(d):
        return reduce (lambda a, b: a + b, (l['line'] for l in d['lines'])) + bytearray((0xff,0xff))

    chv_file = parse_file(chv_desc, FILENAME)
    all_eles = [ele_content_from_dict(d) for d in chv_file['glyphs']]

    for e in all_eles:
        draw_ele(e)
        print '-' * 20
        

