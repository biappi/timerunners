import socket
import cmd
import pprint
import sys
import imageutils

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

    def do_vgascreen(self, line):
        data    = self.cli.command('showmemory a000:0000 fa00')
        palette = self.cli.command('dumppal')

        def yield_color_bytes():
            for i, l in enumerate(data.splitlines()):
                if not l.startswith('O:'):
                    continue

                l = l[15:]  # strips 'O: A000:XXXX  '

                for byte in l.split():
                    yield int(byte, 16)

        image = imageutils.Image(320, 200, yield_color_bytes())
        pal   = [i[3:] for i in palette.splitlines() if i.startswith('O:')]

        image.show(pal)

    def default(self, line):
        if line == 'EOF':
            print
            print "Bye"
            sys.exit(0)

        print self.cli.command(line)

if __name__ == '__main__':
    dbg = Debugger()
    dbg.cmdloop()
