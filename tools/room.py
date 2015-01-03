from dumper import *
from ele import ele_desc, draw_ele

FILENAME = "../original/GAME_DIR/AR1/MAP/ROOM.ROE"

room_desc = (
    (array, 'rooms', {

        'items_struct': (
            (string, 'ROOM', {'length': fixed(4) }),
            (array, 'mat_files', {
                'items_struct': (
                    (uint8, 'info'),
                    (uint8, 'file_number'),
                ),
                'items': fixed(0x10),
            }),
            (array, 'tiles', {
                'items_struct': (
                    (array, 'rows', {
                        'items_struct': (
                            (uint8, 'flip'),
                            (uint8, 'tile'),
                        ),
                        'items': fixed(0x13),
                    }),
                ),
                'items': fixed(0x13),
            }),
            (string, 'unknown', ({'length': fixed(0x1fe), 'binary': fixed(True)})),
        ),
        'items': fixed(44),

    }),
)

if __name__ == '__main__':
    dump_file(room_desc, FILENAME)

