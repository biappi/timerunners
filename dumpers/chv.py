from dumper import *

FILENAME = "../original/GAME_DIR/FNT/MANAGER.CHV"

chv_desc = (
    (uint8, 'first_char'),
    (uint8, 'last_char'),
    (uint8, 'unknown1'),
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

dump_file(chv_desc, FILENAME)


