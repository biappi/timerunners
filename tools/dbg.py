import socket
import cmd
import pprint
import sys
import imageutils
import dumper

import readline

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

def decode(data, cs, ip):
    from pymsasid import pymsasid
    from dbg_asm_syntax import syntax

    base = (cs << 8) + ip

    class x: pass
    string_data = [chr(i) for i in data]
    self = x()
    self.input = pymsasid.Input(pymsasid.BufferHook, string_data, base)
    self.pc = base
    self.error = 0

    self.dis_mode = 16
    self.syntax = syntax

    i = 0
    try:
        while self.pc < base + len(data) and not self.error:
            inst = pymsasid.dec.decode(self)

            self.pc = inst.pc
            inst_ip = self.pc - (cs << 8)
            print '%04X:%04X | %s' % (cs, inst_ip, inst)

            i += 1
            if i == 20:
                break
    except:
        pass

class Client(object):
    def __init__(self, host='localhost', port=6969):
        self.s = socket.socket()
        self.s.connect((host, port))
        print self.s.recv(4096)

    def command(self, cmd):
        self.s.sendall(cmd + '\n')
        return self.listen_response()

    def listen_response(self):
        sofar = ''

        while True:
            sofar += self.s.recv(4096)
            if sofar.splitlines()[-1].startswith('C: '):
                return sofar

class Debugger(cmd.Cmd):
    def __init__(self, host='localhost', port=6969):
        cmd.Cmd.__init__(self)
        self.cli = Client(host, port)
        self.post_cmd('')

    def post_cmd(self, line):
        cpu = self.get_registers()
        self.prompt = '%04x:%04x ] ' % (cpu['cs'], cpu['eip'])

    def get_data(self, address, size):
        data_string = self.cli.command('showmemory %s %x' % (address, size))
        data = bytearray(size)
        data_offset = 0

        for l in data_string.splitlines():
            if l.startswith('O:'):
                l = l[15:]  # strips 'O: A000:XXXX  '

                for byte in l.split():
                    data[data_offset] = int(byte, 16)
                    data_offset += 1
    
        return data

    def get_registers(self):
        registers = {}
        registers_string = self.cli.command('showregisters')

        for line in registers_string.splitlines():
            if line.startswith('O: '):
                name, value = line[3:].split(': ')
                try:    value = int(value, 16)
                except: pass
                registers[name] = value

        return registers
        
    def do_vgascreen(self, line):
        bitmap  = self.get_data('a000:0000', 0xfa00)

        palette = self.cli.command('dumppal')
        palette = [i[3:] for i in palette.splitlines() if i.startswith('O:')]

        image   = imageutils.Image(320, 200, bitmap, palette)

        image.show()

    def do_registers(self, cmd):
        import pprint
        pprint.pprint(self.get_registers())

    def do_disass(self, cmd):
        reg = self.get_registers()
        data = self.get_data('%04x:%04x' % (reg['cs'], reg['eip']), 50)
        print
        decode(data, reg['cs'], reg['eip'])
        print

    def default(self, line):
        if line == 'EOF':
            print
            print "Bye"
            sys.exit(0)

        print self.cli.command(line)

if __name__ == '__main__':
    dbg = Debugger()
    try:
        dbg.cmdloop()
    except KeyboardInterrupt:
        print
        print "Fuckoff"
        sys.exit()

