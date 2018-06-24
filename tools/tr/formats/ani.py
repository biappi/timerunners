from tr import dumpers

from ..utils.imageutils import Image
import sys

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

def main(args):
    try:
        x = dumpers.parse_file(dumpers.ani.desc, args[2])
    except:
        x = dumpers.parse_file(dumpers.ani.desc, dumpers.ani.FILENAME)

    pal = map(color_dict_to_string, x['palette'][0]['colors'])

    for ele in x['frames']:
        img = draw_ani_ele(ele)
        img.show(pal, 2)
