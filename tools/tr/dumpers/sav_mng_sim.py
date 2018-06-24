from dumper import *

FILENAME = "../original/SAVEGAME/SAV0MNG1.SIM"

desc = (
    (padding, 'thumbnail', { 'size':   fixed(0x1c06) }),
    (string,  'name',      { 'length': fixed(0x15), 'pascal': fixed(True) }),
    (padding, 'palette',   { 'size':   fixed(0x300)  }),
    (uint8,   'stack_size'),
    (array,   'task_stack', {
        'items_struct': (
            (uint16, 't'),
        ),
        'items': relative('.stack_size'),
    }),
    (array,   'first_block_swivar', {
        'items_struct': (
            (uint32, 't'),
        ),
        'items': fixed(0x400),
    }),
    (array,   'second_block_swivar', {
        'items_struct': (
            (uint8, 't'),
        ),
        'items': fixed(0x40),
    })
)

