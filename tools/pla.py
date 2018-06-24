import sys
import os

# F000:14CB                   ] break CODS_PLAYER.EXE:seg005:1a2
# CODS_PLAYER.EXE:seg008:1337 ] iv ds:22fe current_tok
# CODS_PLAYER.EXE:seg005:01A2 ] iv ds:2300 off
 
try:
    filename = sys.argv[1]
except:
    filename = '../original/GAME_DIR/PLR/PLA/AN00.PLA'

TEXTS_IT    = "../original/GAME_DIR/PTX/Texts.kit"

def pti_file_to_dict(content):
    lines = {}
    for block in content['pti_blocks']:
        for line in block['lines']:
            n, l = line['line_id'], line['line']
            lines[n] = l

    return lines

def load_text_file(filename):
    texts_it = parse_file(pti_desc, filename)
    return pti_file_to_dict(texts_it)

try:
    texts = load_text_file(TEXTS_IT)
except:
    pass

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

opcode_names = {
    0x0001: ("init", ('width', 'height', 'unk')),
    0x0003: ("load_ani", ('ani_file', 'unk')),
    0x0009: ("set_swivar", ('swi', 'val')),
    0x0019: ("load_font", ('font_file')),
    0x000a: ("end", ()),
    0x0023: ("load_ptr", ('ptr_file')),
    0x0028: ("load_til", ('til_file', 'unk')),
    0x0029: ("load_texts", ('text_file')),
    0x002e: ("set_text_bounds", ('unk', 'width', 'height')),
    0x0031: ("set_text_color", ('unk', 'r', 'g', 'b')),
}

names_by_code = { v[0] : k for k, v in opcode_names.iteritems() }

class Asm:
    def __init__(self):
        self.buf = ""

    def __getattr__(self, name):
        if name.startswith('op_'):
            try: op = int(name[3:7], 16)
            except: raise Exception("incorrect opcode number")
        elif names_by_code.get(name, None) is not None:
            op = names_by_code[name]
        else:
            raise Exception("unknown opcode - " + name)


        try: sig = tokens[op]
        except: raise Exception("incorrect opcode")

        return self.opcode_func(op, sig)

    def opcode_func(self, opcode, sig):
        def inner(*args):
            self.emit_start_token(opcode)

            if sig is None:
                return

            if len(args) != len(sig):
                raise Exception("incorrect nr of args")

            for i, arg in zip(sig, args):
                getattr(self, "emit_%s" % i.__name__)(arg)

        return inner

    def emit_start_token(self, opcode):
        self.emit_next_int16(opcode)

    def emit_next_int16(self, arg):
        self.buf += chr((arg & 0xff00) >> 8)
        self.buf += chr((arg & 0x00ff) >> 0)

    def emit_next_int32(self, arg):
        self.buf += chr((arg & 0xff000000) >> 24)
        self.buf += chr((arg & 0x00ff0000) >> 16)
        self.buf += chr((arg & 0x000000ff) >>  0)
        self.buf += chr((arg & 0x0000ff00) >>  8)

    def emit_next_string(self, arg):
        self.buf += arg
        self.buf += chr(0)

        if ((len(arg) + 1) % 2) != 0:
            self.buf += chr(0)

    def run(self):
        f = file("../original/GAME_DIR/PLR/PLA/LOGO.PLA", "w")
        f.write(self.buf)
        f.close()
        os.system("cd ../ && ../dosbox-dump/dosbox original/MANAGER.EXE")

    def dump(self):
        sys.stdout.write(self.buf)
        

def disassa():
    intro_pla = [ord(i) for i in open(filename).read()]
    i = enumerate(iter(intro_pla))

    while True:
        nbyte, opcode = next_int16(i)
        print "%04x - %04x" % (nbyte, opcode),

        args_constr = tokens[opcode]
        if args_constr is None:
            print
            break

        args = (constr(i) for constr in args_constr)

        print ', '.join(repr(j) for _, j in args)


def disassapy():
    intro_pla = [ord(i) for i in open(filename).read()]
    i = enumerate(iter(intro_pla))

    print 'import pla'
    print
    print 'a = pla.Asm()'
    print
    while True:
        nbyte, opcode = next_int16(i)

        args_constr = tokens[opcode]
        if args_constr is None:
            name = opcode_names.get(opcode, ('op_%04x' % opcode, None))[0]
            print "a.%s()" % (name)
            break

        args = [constr(i) for constr in args_constr]

        py_args = []

        for arg_, sig_ in zip(args, args_constr):
            arg, sig = arg_[1], sig_.__name__

            if sig == 'next_int16':
                py_args.append("%d" % arg)
            elif sig == 'next_int32':
                py_args.append("%d" % arg)
            elif sig == 'next_string':
                py_args.append("'%s'" % arg)

        name = opcode_names.get(opcode, ('op_%04x' % opcode, None))[0]
        print "a.%s(%s)" % (name, ', '.join(py_args))

    print
    print 'a.run()'

if __name__ == '__main__':
    disassapy()


