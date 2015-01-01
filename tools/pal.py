from dumper import *

FILENAME = "../original/MANAGER.PAL"
FILENAME = "../original/GAME_DIR/AR1/STA/ARCADE.PAL"

pal_desc = (
    (uint8,   'first_color'),
    (uint8,   'count'),
    (padding, 'unused', {'size': fixed(2) }),
    (uint8,   'must_be_80'),
    (array,   'palette', {
        'items_struct': (
            (uint8, 'r'),
            (uint8, 'g'),
            (uint8, 'b'),
        ),
        'items_including': relative('.count'),
    }),
)

def load_palette(filename):
    pal = parse_file(pal_desc, filename)

    def color_dict_to_string(c):
        return "#%02x%02x%02x" % (c['r'] << 2, c['g'] << 2, c['b'] << 2)

    palette = ['#000000'] * 256
    first_color = pal['first_color']
    for i, color in enumerate(pal['palette']):
        palette[first_color + i] = color_dict_to_string(color)

    return palette

if __name__ == '__main__':
    dump_file(pal_desc, FILENAME)



