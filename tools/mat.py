from imageutils import Image
from pal import load_palette
from dumper import *

FILENAME = "../original/GAME_DIR/AR1/STA/BUFFER1.MAT"

mat_desc = (
    (array, 'tiles', {
        'items': fixed((320 * 200) / (16 * 10)),
        'items_struct': (
            (array, 'rows', {
                'items': fixed(10),
                'items_struct': (
                    (array, 'row', {
                        'items' : fixed(16),
                        'items_struct': (
                            (uint8, 'p'),
                        ),
                    }),
                )
            }),
        ),
    }),
)

dump_file(mat_desc, FILENAME)
