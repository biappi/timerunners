from dumper import *
import sys

FILENAME = "../original/SAVEGAME/SAV0MNG1.SIM"

sav_mng_desc = (
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

try:
    dump_file(sav_mng_desc, sys.argv[1])
except:
    dump_file(sav_mng_desc, FILENAME)


