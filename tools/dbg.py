import socket
import cmd
import pprint
import sys
import imageutils
import readline

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

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

    def do_vgascreen(self, line):
        bitmap  = self.get_data('a000:0000', 0xfa00)

        palette = self.cli.command('dumppal')
        palette = [i[3:] for i in palette.splitlines() if i.startswith('O:')]

        image   = imageutils.Image(320, 200, bitmap, palette)

        image.show()

    def default(self, line):
        if line == 'EOF':
            print
            print "Bye"
            sys.exit(0)

        print self.cli.command(line)

if __name__ == '__main__':
    dbg = Debugger()
    dbg.cmdloop()