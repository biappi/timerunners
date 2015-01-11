from dumper import *

FILENAME = "../original/GAME_DIR/PTX/Texts.kit"

pti_desc = (
    (string,  'header_simul', {'length': fixed(0x40)}),
    (array,   'infos', {
        'items_struct': (
            (uint16, 'first_line_in_this'),
            (uint16, 'first_line_in_next'),
            (uint16, 'nr_of_lines'),
            (uint16, 'size_in_disk'),
            (uint32, 'offset'),
        ),
        'items': fixed(0x10),
    }),
    (uint16,  'header_unknown1'),
    (uint8,   'header_xor_key'),
    (uint8,   'header_unknown2'),
    (padding, 'header_end_pad', {'size': fixed(0x40)}),
    (block,   'pti_blocks', {
        'offset': relative('.infos.{i}.offset'),
        'items_struct': (
            (array, 'lines', {
                'items_struct': (
                    (uint16, 'line_id'),
                    (uint8,  'length'),
                    (string, 'line', {'length': relative('length'),
                                      'xor':    relative('.header_xor_key')}),
                    (uint8,  'unknown'),
                ),
                'items': relative('.infos.{i}.nr_of_lines'),
            }),
        ),
        'count': fixed(0x10),
        'ignore_if_zero': relative('.infos.{i}.first_line_in_this'),
    })
)

if __name__ == '__main__':
    dump_file(pti_desc, FILENAME)
