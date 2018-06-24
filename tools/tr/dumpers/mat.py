from dumper import *

FILENAME = "../original/GAME_DIR/AR1/STA/BUFFER1.MAT"

TILE_W = 16
TILE_H = 10

desc = (
    (array, 'tiles', {
        'items': fixed((320 * 200) / (16 * 10)),
        'items_struct': (
            (array, 'rows', {
                'items': fixed(TILE_H),
                'items_struct': (
                    (array, 'row', {
                        'items' : fixed(TILE_W),
                        'items_struct': (
                            (uint8, 'p'),
                        ),
                    }),
                )
            }),
        ),
    }),
)
