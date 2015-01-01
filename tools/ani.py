from dumper import *

FILENAME = "../original/GAME_DIR/PLR/BNK/LOGO.ANI"

ani_desc = (
    (uint16,   'unused1'),
    (uint16,   'count'),
    (uint16,   'size_in_memory'),
    (uint16,   'unused2'),
    (uint16,   'unused3'),
    (array,    'items', {
        'items_struct': {
            (uint32, 'boh'),
        },
        'items': relative('count'),
    }),
    (string,   'buffer', {
        'length': relative('size_in_memory'),
        'binary': fixed(True),
    }),
)

dump_file(ani_desc, FILENAME)


