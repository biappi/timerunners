import matplotlib.pyplot as plt


def FILENAME(x): return "../original/GAME_DIR/INS/%s" % x


class Wavino(object):
    def __init__(self, data):
        self.data = data

    def raw(self):
        data_chunk = []
        fmt_chunk = []
        riff_chunk = []

        def le32(x):
            return [
                (x & 0x000000FF),
                (x & 0x0000FF00) >> 8,
                (x & 0x00FF0000) >> 16,
                (x & 0xFF000000) >> 24
            ]

        def le16(x):
            return [
                (x & 0x00FF),
                (x & 0xFF00) >> 8
            ]

        ld = len(data)
        data_chunk += ['d', 'a', 't', 'a']      # data: Chunk ID
        data_chunk += le32(ld)                  # data: Chunk size
        data_chunk += self.data                 # data: Data

        fmt_chunk += ['f', 'm', 't', ' ']       # fmt: Chunk ID
        fmt_chunk += le32(16)                   # fmt: Chunk size
        fmt_chunk += le16(1)                    # fmt: Audio format (1 = PCM)
        fmt_chunk += le16(1)                    # fmt: Channel number
        fmt_chunk += le32(11050)                # fmt: Sample rate
        fmt_chunk += le32(11050)                # fmt: Byte rate
        fmt_chunk += le16(1)                    # fmt: Block align
        fmt_chunk += le16(8)                    # fmt: Bits per sample

        tot_len = len(data_chunk) + len(fmt_chunk) + 4
        riff_chunk += ['R', 'I', 'F', 'F']      # RIFF: Chunk ID
        riff_chunk += le32(tot_len)             # RIFF: Chunk size
        riff_chunk += ['W', 'A', 'V', 'E']      # RIFF: File format

        return bytearray(riff_chunk + fmt_chunk + data_chunk)

def main(*args):
    for fid in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '0A']:
        with open(FILENAME(fid), 'rb') as f:
            data = [ord(i) for i in f.read()]
            # plt.plot([x if x < 128 else x-255 for x in data])
            # plt.show()

            with open(FILENAME(fid) + '.wav', 'wb') as w:
                w.write(Wavino(
                    [128 + (x if x < 128 else x - 255) for x in data]).raw())
