from tr import dumpers

from ele import draw_ele

def main(*args):
    chv_file = dumpers.parse_file(dumpers.chv.desc, dumpers.chv.FILENAME)

    for e in chv_file['glyphs']:
        draw_ele(e)
        print '-' * 20
        

