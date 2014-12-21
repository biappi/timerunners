# yes this is ugly.

FILENAME = "../original/GAME_DIR/PTX/Texts.kit"

def hexdump(data):
    def is_print(c):
        return 0x20 <= c <= 0x7f

    ascii_line = ''
    for i, byte in enumerate(data):
        if (i % 0x10) == 0:
            print '%8x  | ' % i,

        print '%02x' % byte,
        ascii_line += chr(byte) if is_print(byte) else '.'

        if (i % 4) == 3:
            print ' ',

        if (i % 0x10) == 0xf:
            print '|', ascii_line
            ascii_line = ''

    print

def int_f(name, pos, v):
    return "%20s (%8x) ] %x (%d)" % (name, pos, v, v)

class StructDesc(object):
    def __init__(self):
        self.structure = []

    def read(f):
        def wrap(self, name, *args, **kwargs):
            self.structure.append((name, f, args, kwargs))
        return wrap

    def evaluate(self, buf, pos=0, indent=0):
        output = []
        all_size = 0
        struct = {}

        for name, f, args, kwargs in self.structure:
            v, size, desc = f(self, name, buf, pos, *args, indent=indent, struct=struct, **kwargs)

            struct[name] = v

            output.append(('    ' * indent) + desc)
            pos += size
            all_size += size

        return struct, all_size, '\n'.join(output)


    @read
    def padding(self, name, buf, pos, size, **kwargs):
        return 0, size, ''

    @read
    def uint8(self, name, buf, pos, **kwargs):
        v = buf[pos]
        return v, 1, int_f(name, pos, v)

    @read
    def uint16(self, name, buf, pos, **kwargs):
        v  = buf[pos + 0]
        v += buf[pos + 1] <<  8
        return v, 2, int_f(name, pos, v)

    @read
    def uint32(self, name, buf, pos, **kwargs):
        v  = buf[pos + 0]
        v += buf[pos + 1] <<   8
        v += buf[pos + 2] <<  16
        v += buf[pos + 3] <<  24
        return v, 4, int_f(name, pos, v)

    @read
    def array(self, name, buf, pos, items_struct, items=None, items_name=None, indent=0, struct={}):

        if items:
            out = "Fixed array of %d elements\n" % (items)
        elif items_name:
            
            items = struct[items_name]
            out ="variable array of %s (%d) elements\n" % (items_name, items)
            
        size = 0
        result = []
        out = [("%20s (%8x) ] %s" % (name, pos, out))]
        for i in xrange(items):
            out.append(('   ' * (indent + 1)) + 'Item %d:' % i)
            v, s, o = items_struct.evaluate(buf, pos + size, indent + 1)
            result.append(v)
            out.append(o)
            out.append('\n')
            size += s

        return result, size, '\n'.join(out)

    @read
    def string(self, name, buf, pos, length=None, length_name=None, xor=0, struct={}, **kwargs):
        if not length:
            length = struct[length_name]

        v = ''.join(chr(i ^ xor) for i in buf[pos:pos + length])
        desc = "%20s (%8x) ] %s" % (name, pos, v)
        return v, length, desc

    @read
    def data(self, name, buf, pos, length_name=None, struct={}, **kwargs):
        length = struct[length_name]
        v = ''.join(chr(i) for i in buf[pos:pos + length])
        desc = "%20s (%8x) ] %s" % (name, pos, v)
        return v, length, desc

ptifile = open(FILENAME, 'rb').read()
ptifile = [ord(i) for i in ptifile]

# hexdump(ptifile)

infos = StructDesc()
infos.uint16('first_line_in_this')
infos.uint16('first_line_in_next')
infos.uint16('nr_of_lines')
infos.uint16('size_in_disk')
infos.uint32('offset')

pti = StructDesc()
pti.string('header_simul', 0x40)
pti.array('infos', infos, items=0x10)
pti.uint16('header_unknown1')
pti.uint8('header_xor_key')
pti.uint8('header_unknown2')
pti.padding('header_end_pad', 0x40)


obby, sizzi, outti = pti.evaluate(ptifile) # evaluate the header

line = StructDesc()
line.uint16('line_id')
line.uint8('length')
line.string('line', length_name='length', xor=obby['header_xor_key'])
line.uint8('padding')

buff = StructDesc()
buff.array('lines', line, items=obby['infos'][0]['nr_of_lines'])

un, du, tr = buff.evaluate(ptifile, pos=obby['infos'][0]['offset'])

print tr

import pprint
#pprint.pprint(obby)
#print tr
#print outti
#print sizzi
