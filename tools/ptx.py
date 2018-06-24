from dumper import *
import sys

FILENAME = "../original/GAME_DIR/AR1/FIL/PTX"

ptx_desc = (
    (string, 'unknown', {'binary': fixed(True), 'length':fixed(0x10)}),
        (uint16_be, 'count'),
        (array,    'items', {
            'items': relative('count'),
            'items_struct': (
                (uint16_be, 'room_nr'),
                (uint16_be, 'pupo_min_x'),
                (uint16_be, 'pupo_min_y'),
                (uint16_be, 'pupo_max_x'),
                (uint16_be, 'pupo_max_y'),
                (uint16_be, 'nr_items'),
                (array, 'ptis', {
                    'items': fixed(5),
                    'items_struct': (
                        (uint16_be, 'look_in_swi_flag'),
                        (uint16_be, 'pti1'),
                        (uint16_be, 'pti2'),
                    )
                }),
    )}),
)

if __name__ == '__main__':
    try:
        dump_file(ptx_desc, sys.argv[1])
    except:
        dump_file(ptx_desc, FILENAME)


