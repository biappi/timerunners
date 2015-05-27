class Palette:

    class __RGB:

        def __init__(self, r, g, b):
            self.r = r
            self.g = g
            self.b = b

    @staticmethod
    def html_format_raw(raw_data):
        x = raw_data
        return ['#%02x%02x%02x' % (x[i] << 2, x[i+1] << 2, x[i+2] << 2) for i in range(0, len(x), 3)]

    @staticmethod
    def rgb_format_raw(raw_data):
        x = raw_data
        return [Palette.__RGB(x[i] << 2, x[i+1] << 2, x[i+2] << 2) for i in range(0, len(x), 3)]

    @staticmethod
    def html_format_pal(palette_data):
        x = palette_data
        return ['#%02x%02x%02x' % (q['r'] << 2, q['g'] << 2, q['b'] << 2) for q in x]

    @staticmethod
    def rgb_format_pal(palette_data):
        x = palette_data
        return [Palette.__RGB(q['r'] << 2, q['g'] << 2, q['b'] << 2) for q in x]
