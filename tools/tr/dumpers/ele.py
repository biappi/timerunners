from dumper import *

ele_item = (
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
)

desc = (
    (uint16, 'image_count'),
    (array,  'relocations', {
        'items_struct': (
            (uint16, 'off'),
            (uint16, 'seg'),
        ),
        'items': relative('image_count'),
    }),
    (block, 'eles', {
        'offset': add(relative('.relocations.{i}.off'), fixed(2)),
        'items_struct': ele_item,
        'count': relative('image_count'),
    }),
)

