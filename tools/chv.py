from dumper import *
from ele import ele_desc, draw_ele

FILENAME = "../original/GAME_DIR/FNT/INTRO.CHV"

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
        'items_struct': ele_desc,
        'count_including': subtract(relative('.last_char'), relative('.first_char')),
        'ignore_if_FFFF': relative('.relocations.{i}.offset'),
    }),
)

if __name__ == '__main__':
    chv_file = parse_file(chv_desc, FILENAME)

    for e in chv_file['glyphs']:
        draw_ele(e)
        print '-' * 20
        

