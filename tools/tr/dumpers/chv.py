from dumper import *
import ele

FILENAME = "../original/GAME_DIR/FNT/INTRO.CHV"

desc  = (
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
        'items_struct': ele.ele_item,
        'count_including': subtract(relative('.last_char'), relative('.first_char')),
        'ignore_if_FFFF': relative('.relocations.{i}.offset'),
    }),
)
