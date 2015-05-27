class Bitmappe:

    @staticmethod
    def b16(x):
        return [(x & (0x000000FF << i)) >> i for i in range(0, 16, 8)]

    @staticmethod
    def b32(x):
        return [(x & (0x000000FF << i)) >> i for i in range(0, 32, 8)]

    @staticmethod
    def to_file(palette, data, width, height, fname, bpp=24):
        header_size = 40 + 14

        #print len(data[0]), [palette[int(x)] for x in data[0]]

        pixel_array = bytearray([]).join(
            bytearray([]).join(
                [bytearray([r, g, b]) for (r, g, b) in [palette[int(x)] for x in line]] +
                [bytearray([] if not len(line) % 4 else [0] * (4 - (len(line) % 4)))]
            )
            for line in data[::-1]
        )

        file_size = header_size + len(pixel_array)

        self = Bitmappe

        header = bytearray([]).join([
            bytearray([0x42, 0x4d]),                # Signature
            bytearray(self.b32(file_size)),         # File size (unreliable)
            bytearray(self.b32(0)),                 # Reserved, must be zero
            bytearray(self.b32(header_size)),       # Offset to the pixel array in bytes
            bytearray(self.b32(40)),                # Size of BITMAPINFOHEADER structure, must be 40
            bytearray(self.b32(width)),             # Width
            bytearray(self.b32(height)),            # Height
            bytearray(self.b16(1)),                 # Number of planes in the image, must be 1
            bytearray(self.b16(bpp)),               # bits per pixel (1, 4, 8, or 24)
            # BMP3 headers
            bytearray(self.b32(0)),                 # Compression type (0=none, 1=RLE-8, 2=RLE-4)
            bytearray(self.b32(len(pixel_array))),  # Size of image data in bytes (including padding)
            bytearray(self.b32(0)),                 # Horizontal resolution in pixels per meter (unreliable)
            bytearray(self.b32(0)),                 # Vertical resolution in pixels per meter (unreliable)
            bytearray(self.b32(0)),                 # Number of colors in image, or zero
            bytearray(self.b32(0)),                 # Number of important colors, or zero
            # BMP4 headers
            # bytearray([0xff, 0x00, 0x00, 0x00]),    # Red mask
            # bytearray([0x00, 0xff, 0x00, 0x00]),    # Green mask
            # bytearray([0x00, 0x00, 0xff, 0x00]),    # Blue mask
            # bytearray([0x00, 0x00, 0x00, 0xff]),    # Alpha mask
            # bytearray(self.b32(1)),                 # Color space type 00h (calibrated RGB), 01h (device-dependent RGB), and 02h (device-dependent CMYK)
            # bytearray(self.b32(0)),                 # X coordinate of red endpoint (not significant in this case)
            # bytearray(self.b32(0)),                 # Y coordinate of red endpoint (not significant in this case)
            # bytearray(self.b32(0)),                 # Z coordinate of red endpoint (not significant in this case)
            # bytearray(self.b32(0)),                 # X coordinate of green endpoint (not significant in this case)
            # bytearray(self.b32(0)),                 # Y coordinate of green endpoint (not significant in this case)
            # bytearray(self.b32(0)),                 # Z coordinate of green endpoint (not significant in this case)
            # bytearray(self.b32(0)),                 # X coordinate of blue endpoint (not significant in this case)
            # bytearray(self.b32(0)),                 # Y coordinate of blue endpoint (not significant in this case)
            # bytearray(self.b32(0)),                 # Z coordinate of blue endpoint (not significant in this case)
            # bytearray(self.b32(0)),                 # Gamma red coordinate scale value
            # bytearray(self.b32(0)),                 # Gamma green coordinate scale value
            # bytearray(self.b32(0)),                 # Gamma blue coordinate scale value
        ])

        print len(header)

        assert len(header) == header_size

        with open(fname, 'w+') as f:
            f.write(header)       # Writing header
            f.write(pixel_array)  # Writing data
