from tr import dumpers

FILENAME = "../original/MANAGER.PAL"
FILENAME = "../original/GAME_DIR/AR1/STA/ARCADE.PAL"

def load_palette(filename):
    pal_file = dumpers.parse_file(dumpers.pal.desc, filename)

    def color_dict_to_string(c):
        return "#%02x%02x%02x" % (c['r'] << 2, c['g'] << 2, c['b'] << 2)

    palette = ['#000000'] * 256
    first_color = pal_file['first_color']
    for i, color in enumerate(pal_file['palette']):
        palette[first_color + i] = color_dict_to_string(color)

    return palette

