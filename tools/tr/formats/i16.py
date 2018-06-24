from tr import dumpers

from ele import draw_ele, show_ele


def main(*args):
    i16_file = dumpers.parse_file(dumpers.i16.desc, dumpers.i16.FILENAME)

    def color_dict_to_string(c):
        return "#%02x%02x%02x" % (c['r'] << 2, c['g'] << 2, c['b'] << 2)

    first_color = i16_file['palette'][0]['first_color']
    palette = ['#000000'] * 256
    for i, color in enumerate(i16_file['palette'][0]['colors']):
        palette[first_color + i] = color_dict_to_string(color)

    show_ele(i16_file['first_ele'][0], palette, 0xf0 , 3)
    show_ele(i16_file['second_ele'][0], palette, 0xf0, 3)

    """
    print
    draw_ele(i16_file['first_ele'][0])

    print
    draw_ele(i16_file['second_ele'][0])
    """

