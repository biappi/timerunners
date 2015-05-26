import sys

# F000:14CB                   ] break CODS_PLAYER.EXE:seg005:1a2
# CODS_PLAYER.EXE:seg008:1337 ] iv ds:22fe current_tok
# CODS_PLAYER.EXE:seg005:01A2 ] iv ds:2300 off
 
try:
    filename = sys.argv[1]
except:
    filename = '../original/GAME_DIR/PLR/PLA/INTRO.PLA'

def next_int16(i):
    first_i,  first_b  = next(i)
    second_i, second_b = next(i)

    return first_i, ((first_b << 8) + second_b)

def next_int32(i):
    first_i,  first_b  = next(i)
    second_i, second_b = next(i)
    third_i,  third_b  = next(i)
    fourth_i, fourth_b = next(i)

    r = ((first_b  << 24) +
         (second_b << 16) +
         (third_b  <<  8) +
         (fourth_b <<  0))

    return first_i, r


def next_string(i):
    offset, char  = next(i)

    s = []

    while char != 0:
        s.append(chr(char))
        _, char = next(i)

    if (offset + len(s) + 1) & 1:
        next(i)

    return offset, ''.join(s)

tokens = {
    # from intro.pla

    0x0001: (
        next_int16,
        next_int16,
        next_int16,
    ),

    0x0023: (
        next_string,
    ),

    0x0029: (
        next_string,
    ),

    0x0028: (
        next_string,
        next_int16,
    ),

    0x0019: (
        next_string,
    ),

    0x0031: (
        next_int16,
        next_int16,
        next_int16,
        next_int16,
    ),

    0x0032: (
        next_int16,
    ),

    0x0003: (
        next_string,
        next_int16,
    ),

    0x0004: (
        next_int16,
        next_int16,
        next_int16,
        next_int16,
        next_int16,
    ),

    0x0010: (
        next_int16,
        next_int16,
        next_int16,
    ),

    0x0007: (
        next_int16,
    ),

    0x002e: (
        next_int16,
        next_int16,
        next_int16,
    ),

    0x002a: (
        next_int16,
        next_int16,
    ),

    0x002c: (
        next_int16,
        next_int16,
        next_int16,
        next_int16,
    ),

    0x002d: (
        next_int16,
    ),

    0x0011: (
        next_int16,
        next_int16,
    ),

    0x0006: (
        next_int16,
    ),

    0x000a: None,

    # from ani00.pla

    0x0009: (
        next_int16,
        next_int32,
    ),

    0x001c: (
        next_string,
    ),

    0x000b: (
        next_int16,
    ),

    0x000e: (
        next_int16,
        next_int16,
        next_int32,
    ),

    0x000f: (
        next_int16,
    ),

    0x000c: (
        next_int16,
    ),

    0x0013: (
        next_string,
    ),
}


intro_pla = [ord(i) for i in open(filename).read()]
i = enumerate(iter(intro_pla))

while True:
    nbyte, opcode = next_int16(i)
    print "%04x - %04x" % (nbyte, opcode),

    args_constr = tokens[opcode]
    if args_constr is None:
        break

    args = (constr(i) for constr in args_constr)

    print ', '.join(repr(j) for _, j in args)
