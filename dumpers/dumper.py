# yes this is ugly.

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
    return "%08x %-35s ]" % (pos, name)

def int_f(name, pos, v):
    return "%s %x (%d)" % (loc_f(name, pos), v, v)

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
            comps = name.split('.')
            abs_name = comps[-1]
            prefix = '.'.join(comps[0:-1])
            return loc(abs_name, prefix)
        else:
            return loc(name, self.prefix)

class value(object):
    def get_in(self, context, loc):
        raise # return None - to subclass

class relative(value):
    def __init__(self, loc):
        self.loc = loc

    def get_in(self, context, base_loc):
        x = str(base_loc.resolve(self.loc))

        for key, text in context['__SUBSTS__'].iteritems():
            x = x.replace(('{%s}' % key), str(text))

        return context[x]

class fixed(value):
    def __init__(self, v):
        self.v = v

    def get_in(self, context, loc, subst={}):
        return self.v

def evaluate(struct_desc, buf, pos=0):
    context = {}
    context['__SUBSTS__'] = {}
    return struct(loc(), struct_desc, buf, pos, context)

class counter_buffer(object):
    def __init__(self, b):
        self.backing = b
        self.what_was_read = bytearray(len(self.backing))

    def __len__(self):
        return len(self.backing)

    def __getitem__(self, key):
        if isinstance(key, int):
            self.what_was_read[key] = 1
            return self.backing[key]
        if isinstance(key, slice):
            result = self.backing[key]
            self.what_was_read[key] = (1,) * len(result)
            return result

    def summary(self):
        read = 0
        not_read = 0

        for i in self.what_was_read:
            if i == 0:
                not_read += 1
            if i == 1:
                read += 1
        
        print 'read %d (%.1f%%) - not read %d - total %d' % (read, read / float(len(self.backing)) * 100, not_read, len(self.backing))

def dump_file(desc, path):
    buf = open(path, 'rb').read()
    buf = [ord(i) for i in buf]
    buf = counter_buffer(buf)
    deserialized, size, dump_string = evaluate(desc, buf)
    print dump_string
    print
    buf.summary()


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

def block(loc, buf, pos, offset=None, items_struct=None, count=None, ignore_if_zero=None, context={}):
    result = []
    out = []
    size = 0

    count = count.get_in(context, loc)
    for i in xrange(count):
        context['__SUBSTS__']['i'] = i

        if ignore_if_zero and (ignore_if_zero.get_in(context, loc) == 0):
            continue

        pos = offset.get_in(context, loc) 
        v, s, o = struct(loc.append(i), items_struct, buf, pos, context=context)
        result.append(v)
        out.append(o)

        size += s
    return result, size, '\n'.join(out)
        
def string(loc, buf, pos, length, xor=fixed(0), context={}, **kwargs):
    length = length.get_in(context, loc)
    xor = xor.get_in(context, loc)
    v = ''.join(chr(i ^ xor) for i in buf[pos:pos + length])
    desc = "%s %s" % (loc_f(loc, pos), v)
    return v, length, desc
