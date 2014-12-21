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

########################

def evaluate(struct_desc, buf, pos=0, indent=0):
    context = {}
    return struct(None, struct_desc, buf, pos, indent, context)

def struct(name, struct_desc, buf, pos=0, indent=0, context={}):
    output = []
    all_size = 0
    for field_desc in struct_desc:
        type_func, name = field_desc[:2]

        try:    kwargs = field_desc[2]
        except: kwargs = {}

        v, size, desc = type_func(name, buf, pos, indent=indent, struct=context, **kwargs)

        context[name] = v

        output.append(('    ' * indent) + desc)
        #print ('    ' * indent) + desc
        pos += size
        all_size += size

    return context, all_size, '\n'.join(output)


def padding(name, buf, pos, size, **kwargs):
    return 0, size, ''

def uint8(name, buf, pos, **kwargs):
    v = buf[pos]
    return v, 1, int_f(name, pos, v)

def uint16(name, buf, pos, **kwargs):
    v  = buf[pos + 0]
    v += buf[pos + 1] <<  8
    return v, 2, int_f(name, pos, v)

def uint32(name, buf, pos, **kwargs):
    v  = buf[pos + 0]
    v += buf[pos + 1] <<   8
    v += buf[pos + 2] <<  16
    v += buf[pos + 3] <<  24
    return v, 4, int_f(name, pos, v)

def array(name, buf, pos, items_struct={}, items=None, items_name=None, indent=0, struct={}):

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
        v, s, o = evaluate(items_struct, buf, pos + size, indent + 1)
        result.append(v)
        out.append(o)
        out.append('\n')
        size += s

    return result, size, '\n'.join(out)

def string(name, buf, pos, length=None, length_name=None, xor=0, struct={}, **kwargs):
    if not length:
        length = struct[length_name]

    v = ''.join(chr(i ^ xor) for i in buf[pos:pos + length])
    desc = "%20s (%8x) ] %s" % (name, pos, v)
    return v, length, desc

def data(name, buf, pos, length_name=None, struct={}, **kwargs):
    length = struct[length_name]
    v = ''.join(chr(i) for i in buf[pos:pos + length])
    desc = "%20s (%8x) ] %s" % (name, pos, v)
    return v, length, desc

###########

ptifile = open(FILENAME, 'rb').read()
ptifile = [ord(i) for i in ptifile]

# hexdump(ptifile)

pti_desc = (
    (string,  'header_simul', {'length': 0x40}),
    (array,   'infos', {
        'items_struct': (
            (uint16, 'first_line_in_this'),
            (uint16, 'first_line_in_next'),
            (uint16, 'nr_of_lines'),
            (uint16, 'size_in_disk'),
            (uint32, 'offset'),
        ),
        'items': 0x10,
    }),
    (uint16,  'header_unknown1'),
    (uint8,   'header_xor_key'),
    (uint8,   'header_unknown2'),
    (padding, 'header_end_pad', {'size': 0x40}),
)

obby, sizzi, outti = evaluate(pti_desc, ptifile) # evaluate the header
print outti

pti_block = (
    (array, 'lines', {
        'items_struct': (
            (uint16, 'line_id'),
            (uint8,  'length'),
            (string, 'line', {'length_name': 'length', 'xor':obby['header_xor_key']}),
            (uint8,  'unknown'),
        ),
        'items': obby['infos'][0]['nr_of_lines'],
    }),
)

un, du, tr = evaluate(pti_block, ptifile, pos=obby['infos'][0]['offset'])

print tr

import pprint
#pprint.pprint(obby)
#print tr
#print outti
#print sizzi
