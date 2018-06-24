from dumper import *

FILENAME = "../original/GAME_DIR/AR1/MAP/ROOM.ROE"

ROOM_W = 0x14
ROOM_H = 0x14

real_size_of_rooms   = 0x4f4
real_number_of_rooms = 44

desc = (
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

            (string, 'unk', {'length':fixed(0x20), 'binary':fixed(True)}),

            (array, 'tile_types', {
                'items_struct': (
                    (array, 'rows', {
                        'items_struct': (
                            (uint8, 'tiletype'),
                        ),
                        'items': fixed(ROOM_W),
                    }),
                ),
                'items': fixed(ROOM_H),
            }),

        ),
        'items': fixed(44),
    }),
)
