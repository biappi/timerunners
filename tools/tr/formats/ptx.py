from tr import dumpers
from pti import pti_file_to_dict

def print_all_hints(hints, texts):
    for hint in hints['items']:
        room_nr = hint['room_nr']
        min_x   = hint['pupo_min_x']
        min_y   = hint['pupo_min_y']
        max_x   = hint['pupo_max_x']
        max_y   = hint['pupo_max_y']

        print 'Room %2d - (%3d, %3d), (%3d, %3d)' % (room_nr, min_x, min_y, max_x, max_y)

        for i in xrange(hint['nr_items']):
            pti = hint['ptis'][i]
            swi  = pti['look_in_swi_flag']
            pti1 = pti['pti1']
            pti2 = pti['pti2']
            print '  swi: %04x' % swi
            print '    1.', texts[pti1]
            print '    2.', texts[pti2]

def main(*args):
    texts = dumpers.parse_file(dumpers.pti.desc, dumpers.pti.FILENAME)
    texts = pti_file_to_dict(texts)
    hints = dumpers.parse_file(dumpers.ptx.desc, dumpers.ptx.FILENAME)
    print_all_hints(hints, texts)
