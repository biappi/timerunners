from dumper import *
from ele import ele_desc, draw_ele

FILENAME = "../original/GAME_DIR/AR1/MAP/ROOM.ROE"

ROOM_W = 0x14
ROOM_H = 0x14

real_size_of_rooms   = 0x4f4
real_number_of_rooms = 44

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
                            (uint16, 'tileid'),
                        ),
                        'items': fixed(ROOM_W),
                    }),
                ),
                'items': fixed(ROOM_H),
            }),
            (string, 'unknown', ({'length': fixed(0x1b0), 'binary': fixed(True)})),
        ),
        'items': fixed(44),
    }),
)

if __name__ == '__main__':
    dump_file(room_desc, FILENAME)

