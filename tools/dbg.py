import socket
import cmd
import pprint
import sys
import imageutils
import dumper
import select

import readline

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

def decode(data, base, cpu, names):
    from pymsasid import pymsasid

    base = base.linear()

    class x: pass
    string_data = [chr(i) for i in data]
    self = x()
    self.input = pymsasid.Input(pymsasid.BufferHook,
                                string_data,
                                base)
    self.pc = base
    self.error = 0
    self.dis_mode = 16
    self.syntax = None

    instructions = []
    i = 0
    while self.pc < base + len(data) and not self.error:
        try:
            inst = pymsasid.dec.decode(self)
        except:
            self.error = 1
            raise
            break

        inst_ip = Address.from_linear(inst.pc, cpu.cs)
        self_ip = Address.from_linear(self.pc, cpu.cs)

        instructions.append((self_ip, inst))
        self.pc = inst.pc

        i += 1
        if i == 20:
            break

    return instructions

class Client(object):
    def __init__(self, host='localhost', port=6969):
        self.s = socket.socket()
        self.s.connect((host, port))
        print self.s.recv(4096)

    def command(self, cmd):
        self.s.sendall(cmd + '\n')
        resp = self.listen_response()

        output   = []
        cpustate = []
        status   = None

        for l in resp.splitlines():
            code, line = l.split(': ', 1)

            if code == 'O':
                output.append(line)
            elif code == 'S':
                cpustate.append(line)
            elif code == 'C':
                status = line
            elif code == 'U':
                pass # i think it's ok to ignore
        if cpustate:
            cpu = Cpu(cpustate)
        else:
            cpu = None

        return output, cpu

    def listen_response(self):
        sofar = ''

        while True:
            try:
                sofar += self.s.recv(4096)
                if sofar.splitlines()[-1].startswith('C: '):
                    return sofar
            except socket.timeout:
                print 'timeout..'

    def check_unsolicited(self):
        data = ''

        try:
            self.s.settimeout(.2)
            while True:
                data += self.s.recv(4096)
            self.s.settimeout(None)
        except socket.timeout:
            pass

        if not data:
            return None

        cpu = Cpu()
        for l in (l[3:] for l in  data.splitlines() if l.startswith('U: ')):
            cpu.update(l)

        return cpu

class Address(object):
    @staticmethod
    def segoff(seg, off):
        a = Address()
        a.seg = seg
        a.off = off
        return a

    @staticmethod
    def string(s):
        seg, off = s.split(':')
        seg = int(seg, 16)
        off = int(off, 16)
        return Address.segoff(seg, off)

    @staticmethod
    def from_linear(address, seg):
        off = address - (seg << 8)
        return Address.segoff(seg, off)

    def linear(self):
        return (self.seg << 8) + self.off

    def __hash__(self):
        return hash(self.linear())

    def __eq__(self, o):
        return self.linear() == o.linear()

    def __str__(self):
        return '%04X:%04X' % (self.seg, self.off)

class RelocationInfo(object):
    def __init__(self, reloc, segs):
        self.reloc = reloc
        self.segs = {}
        self.names = {}
        for addr, name in segs.iteritems():
            addr = addr # + reloc
            self.segs[addr] = name
            self.names[name] = addr
            print hex(addr), name

class NamesMap(object):
    def __init__(self):
        self.names     = {}
        self.addresses = {}
        self.types     = {}
        self.relocs    = {}

        self.load_all()

    def save_all(self):
        na = { str(a) : self.names[a] for a in self.names }
        ad = { n : str(self.addresses[n]) for n in self.addresses }

        import json
        json.dump(
            {
                'names': na,
                'addresses': ad,
                'types': self.types,
            },
            open('state.json', 'w'),
            indent=4,
            sort_keys=True,
        )

    def load_all(self):
        try:
            import json
            state = json.load(open('state.json', 'r'))

            self.names     = state['names']
            self.addresses = state['addresses']
            self.types     = state['types']

            self.names = { Address.string(a) : self.names[a] for a in self.names }
            self.addresses = { n : Address.string(self.addresses[n]) for n in self.addresses }

        except:
            print 'no load'


    def add(self, address, name):
        if name in self.addresses:
            name = name + '_1'

        self.addresses[name] = address
        self.names[address] = name

    def load(self, filename='timerunners.map', relocate=0):
        return
        f = file(filename, 'r').read().splitlines()
        for line in f:
            try:
                add_str, name = line.split()
            except:
                continue
            add = Address.string(add_str)
            add.seg += relocate
            self.add(add, name)

        print 'Loaded %d names.' % len(self.addresses)
        self.save_all()

    def save(self, filename='timerunners.map'):
        return

        f = file(filename, 'w')
        for addr in sorted(self.names):
            f.write('%s %s\n' % ( addr, self.names[addr]))

    def resolve(self, addr):
        return self.names.get(addr, str(addr))

    def address(self, name):
        return self.addresses[name]

    def symbols(self):
        return self.addresses.iterkeys()

    def set_type(self, name, the_type):
        address = self.addresses.get(name, None)
        if not address:
            print 'No name', name
            return

        existing_type = self.types.get(name, None)
        if existing_type:
            print 'Overwriting existing type', existing_type

        self.types[name] = the_type
        self.save_all()

    def variables(self):
        self.types.iterkeys()


    def address_from_string(self, addr):
        try:
            return self.addresses[addr]
        except KeyError:
            pass

        try:
            exe, segname, off = addr.split(':', 2)
            seg = self.relocs[exe].names[segname]
            off = int(off, 16)
            return Address.segoff(seg, off)
        except ValueError:
            pass
        except KeyError:
            pass

        seg, off = addr.split(':', 1)

        try:
            off = int(off, 16)
            seg = int(seg, 16)

            if off > 0xffff:
                raise ValueError

            if seg > 0xffff:
                raise ValueError

            return Address.segoff(seg, off)
        except:
            return None

    def address_to_string(self, addr):
        try:
            return self.names[addr]
        except KeyError:
            pass

        for exename in self.relocs:
            try:
                seg = self.relocs[exename].segs[addr.seg]
                return '%s:%s:%04X' % (exename, seg, addr.off)
            except KeyError:
                pass

        return str(addr)

    def complete_address(self, partial):
        candidates = [name for name in self.addresses if name.startswith(partial)]

        try:
            exename, seg = partial.split(':')
        except Exception as e:
            exename = partial
            seg = ''

        new_candidates = ('%s:' % exename for exename in self.relocs if exename.startswith(partial))
        candidates.extend(new_candidates)

        try:
            new_candidates = ('%s:%s:' % (exename, i) for i in self.relocs[exename].names if i.startswith(seg))
            candidates.extend(new_candidates)
        except Exception as e:
            pass

        return candidates            
            
    def set_relocations(self, exename, relocation, segs):
        self.relocs[exename.replace('\\', '_')] = RelocationInfo(relocation, segs)

class Cpu(object):
    def __init__(self, as_list=[]):
        self.state = {}
        self.cache = {}

        for i in as_list:
            self.update(i)

    def update(self, line):
        name, value = line.split(': ')
        try:    value = int(value, 16)
        except: pass
        self.state[name] = value
        self.cache = {}

    def __getattr__(self, attr):
        if attr in self.state:
            return self.state[attr]

    @property
    def csip(self):
        add = self.cache.get('csip', None)

        if not add:
            add = Address.segoff(self.cs, self.eip)

        return add

class Debugger(cmd.Cmd):
    def __init__(self, host='localhost', port=6969):
        cmd.Cmd.__init__(self)
        self.cli = Client(host, port)
        self.names = NamesMap()
        self.names.load()
        self.names.save()
        self.names.load('ARCADE.map', 0x321f)
        self.prompt = 'Debuggalo ] '
        self.cpu = None
        self.instructions = []

    def check_unsolicited(self):
        cpu = self.cli.check_unsolicited()
        if cpu:
            self.cpu = cpu

    def postcmd(self, stop, line):
        sys.stdout.write('\n\033[1A')
    
    def command(self, command):
        resp, cpu = self.cli.command(command)

        if cpu:
            self.cpu = cpu

        if self.cpu:
            self.prompt = self.names.address_to_string(self.cpu.csip) + ' ] '

        return resp

    def get_data(self, address, size):
        resp = self.command('showmemory %s %x' % (address, size))
        data = bytearray(size)
        data_offset = 0

        for l in resp:
            l = l[12:]  # strips 'O: A000:XXXX  '

            for byte in l.split():
                data[data_offset] = int(byte, 16)
                data_offset += 1
    
        return data

    def do_continue(self, line): self.default('continue')
    def do_bplist  (self, line): self.default('bplist')

    def do_vgascreen(self, line):
        bitmap  = self.get_data('a000:0000', 0xfa00)

        palette = self.command('dumppal')
        palette = [i for i in palette]

        image   = imageutils.Image(320, 200, bitmap, palette)

        image.show()

    def do_disass(self, cmd):
        self.print_code(True)

    def do_bpm(self, cmd):
        print self.command('bpm ' + str(self.names.address(cmd)))

    def complete_bpm(self, text, line, begidx, endidx):
        return [i for i in self.names.symbols() if i.startswith(text)]

    def do_break(self, cmd):
        addr = self.names.address_from_string(cmd)
        print self.command('bp ' + str(addr))

    def complete_break(self, text, line, begidx, endidx):
        return self.names.complete_address(text)

    def do_print(self, cmd):
        t = self.names.types[cmd]
        print cmd, t, self.names.address(cmd)
        if t == 'byte':
            print repr(self.get_data(self.names.address(cmd), 1))
        elif t == 'word':
            print self.get_data(self.names.address(cmd), 2)
        elif t == 'dword':
            print self.get_data(self.names.address(cmd), 4)

    def complete_print(self, tet, line, bi, ei):
        return [i for i in self.names.variables() if i.startswith(text)]

    def do_byte(self, cmd):
        self.names.set_type(cmd, 'byte')

    def complete_byte(self, text, line, begidx, endidx):
        return [i for i in self.names.symbols() if i.startswith(text)]

    def do_word(self, cmd):
        self.names.set_type(cmd, 'word')

    def complete_word(self, text, line, begidx, endidx):
        return [i for i in self.names.symbols() if i.startswith(text)]

    def do_dword(self, cmd):
        self.names.set_type(cmd, 'dword')

    def complete_dword(self, text, line, begidx, endidx):
        return [i for i in self.names.symbols() if i.startswith(text)]

    def do_step(self, cmd):
        self.command('step')
        self.check_unsolicited()
        self.print_code()

    def do_stepi(self, cmd):
        self.command('stepi')
        self.check_unsolicited()
        self.print_code()

    def default(self, line):
        if line == 'EOF':
            print
            print "Bye"
            sys.exit(0)

        print '\n'.join(self.command(line))

    def print_code(self, force=False):
        from dbg_asm_syntax import asm_syntax # circular dep on Address

        get_instr = True
        get_from  = None

        if not force and self.cpu:
            try:
                addrs = [i[0] for i in self.instructions]
                index = addrs.index(self.cpu.csip)
                get_instr = index > 10
                get_from  = addrs[1]
            except ValueError:
                pass

        if get_instr:
            get_from_str = str(get_from) if get_from else 'cs:ip'
            data = self.get_data(get_from_str, 100) # cs:ip will be parsed by dosbox
            get_from = get_from if get_from else self.cpu.csip
            self.instructions = decode(data, get_from, self.cpu, self.names)

        for addr, inst in self.instructions:
            arrow   = '->' if addr == self.cpu.csip else '  '
            print '   %s  %s | %s' % (arrow, addr, asm_syntax(inst, self.names, self.cpu))

    def do_name(self, cmd):
        print cmd, self.names.address_from_string(cmd)

    def complete_name(self, text, line, begidx, endidx):
        return self.names.complete_address(text)

    def do_get_relocations(self, cmd):
        files = {}

        for line in self.command('showrelocations'):
            filename, info = line.split('; ')
            _, filename = filename.split(': ')

            try:
                the_file = files[filename]
            except:
                the_file = {}
                the_file['segs'] = {}
                files[filename] = the_file

            seg, name = info.split(': ')
            if seg == 'relocation':
                the_file['relocation'] = int(name, 16)
            else:
                the_file['segs'][int(seg, 16)] = name

        for filename in files:
            print 'Relocated', filename, 'at %04x' % files[filename]['relocation']
            self.names.set_relocations(filename, files[filename]['relocation'], files[filename]['segs'])

if __name__ == '__main__':
    dbg = Debugger()
    try:
        dbg.cmdloop()
    except KeyboardInterrupt:
        print
        print "Fuckoff"
        sys.exit()

