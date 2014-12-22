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

def loc_f(name, pos, name_prefix=None):
    if name_prefix is not None:
        name = name_prefix + '.' + name
    return "%08x (%-30s) ]" % (pos, name)

def int_f(name, pos, v):
    return "%s %x (%d)" % (loc_f(name, pos), v, v)

########################

class loc(object):
    def __init__(self, name='', prefix=None):
        self.name = name
        self.prefix = prefix

    def __str__(self):
        if self.prefix is None:
            return self.name
        else:
            return '%s.%s' % (self.prefix, self.name)

    def append(self, name):
        return loc(name, str(self))

    def resolve(self, name):
        if name.startswith('.'):
            return # split string and recombine
        else:
            return loc(name, self.prefix)

class value(object):
    def get_in(self, context, loc):
        raise # return None - to subclass

class relative(value):
    def __init__(self, loc):
        self.loc = loc

    def get_in(self, context, base_loc):
        return context[str(base_loc.resolve(self.loc))]

class fixed(value):
    def __init__(self, v):
        self.v = v

    def get_in(self, context, loc):
        return self.v
    
def evaluate(struct_desc, buf, pos=0):
    context = {}
    return struct(loc(), struct_desc, buf, pos, context)

def struct(loc, struct_desc, buf, pos=0, context={}):
    output = []
    all_size = 0
    result = {}

    for field_desc in struct_desc:
        type_func, field_name = field_desc[:2]

        try:    kwargs = field_desc[2]
        except: kwargs = {}

        field_loc = loc.append(field_name)

        v, size, desc = type_func(field_loc, buf, pos, context=context, **kwargs)
        result[field_name] = v

        context[str(field_loc)] = v

        output.append(desc)

        pos += size
        all_size += size

    return result, all_size, '\n'.join(output)


def padding(loc, buf, pos, size, context=None, **kwargs):
    size = size.get_in(context, loc)
    return 0, size, ('%s Padding (0x%x - %d bytes)' % (loc_f(loc, pos), size, size))

def uint8(loc, buf, pos, **kwargs):
    v = buf[pos]
    return v, 1, int_f(loc, pos, v)

def uint16(loc, buf, pos, **kwargs):
    v  = buf[pos + 0]
    v += buf[pos + 1] <<  8
    return v, 2, int_f(loc, pos, v)

def uint32(loc, buf, pos, **kwargs):
    v  = buf[pos + 0]
    v += buf[pos + 1] <<   8
    v += buf[pos + 2] <<  16
    v += buf[pos + 3] <<  24
    return v, 4, int_f(loc, pos, v)

def array(loc, buf, pos, items=None, items_struct=None, context={}):
    size = 0
    result = []
    out = []

    items = items.get_in(context, loc)

    for i in xrange(items):
        v, s, o = struct(loc.append(str(i)), items_struct, buf, pos + size, context=context)
        result.append(v)
        out.append(o)
        size += s

    return result, size, '\n'.join(out)

def string(loc, buf, pos, length, xor=0, context={}, **kwargs):
    length = length.get_in(context, loc)
    v = ''.join(chr(i ^ xor) for i in buf[pos:pos + length])
    desc = "%s %s" % (loc_f(loc, pos), v)
    return v, length, desc

def data(name, buf, pos, length_name=None, struct={}, **kwargs):
    length = struct[length_name]
    v = ''.join(chr(i) for i in buf[pos:pos + length])
    desc = "%s %s" % (loc_f(name, pos), v)
    return v, length, desc

###########

ptifile = open(FILENAME, 'rb').read()
ptifile = [ord(i) for i in ptifile]

# hexdump(ptifile)

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
)

obby, sizzi, outti = evaluate(pti_desc, ptifile) # evaluate the header
print outti

pti_block = (
    (array, 'lines', {
        'items_struct': (
            (uint16, 'line_id'),
            (uint8,  'length'),
            (string, 'line', {'length': relative('length'), 'xor':obby['header_xor_key']}),
            (uint8,  'unknown'),
        ),
        'items': fixed(obby['infos'][0]['nr_of_lines']),
    }),
)

un, du, tr = evaluate(pti_block, ptifile, pos=obby['infos'][0]['offset'])

print tr

import pprint
#pprint.pprint(obby)
#print tr
#print outti
#print sizzi
