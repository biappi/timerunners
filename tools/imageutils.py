import Tkinter
import os

class Image(object):
    def __init__(self, width, height, data=None, palette=None):
        self.width   = width
        self.height  = height
        self.data    = list(data) if data else [0] * width * height
        self.palette = palette

    def put(self, x, y, c):
        assert x < self.width
        assert y < self.height

        self.data[y * self.width + x] = c

    def tkinter_string(self, palette, mult=1):
        def generate_string():
            for i, color in enumerate(self.data):
                if i % self.width == 0:
                    line = []
                    line.append('{')

                for _ in xrange(mult):
                    line.append(palette[color])

                if i % self.width == self.width - 1:
                    line.append('}')
                    for _ in xrange(mult):
                        for k in line:
                            yield k

        return ' '.join(generate_string())

    def show(self, palette=None, mult=1):
        if palette is None:
            palette = self.palette

        t = Tkinter.Tk()
        t.resizable(0, 0)

        c = Tkinter.Canvas(
            t,
            width=self.width * mult,
            height=self.height * mult,
            highlightthickness=0,
        )

        i = Tkinter.PhotoImage()
        i.put(self.tkinter_string(palette, mult))
        c.create_image(0, 0, image=i, anchor=Tkinter.NW)
        c.pack(expand=True, fill=Tkinter.BOTH)
        t.bind("<Return>", lambda _: t.destroy())

        os.system("""osascript -e 'tell application "System Events"
            set frontmost of processes whose unix id is %d to true
        end tell'""" % os.getpid())

        t.mainloop()

