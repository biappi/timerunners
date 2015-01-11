from dumper import parse_file
from imageutils import Image

from pal  import load_palette
from pti  import pti_desc
from room import room_desc, ROOM_W, ROOM_H
from mat  import mat_desc, TILE_H, TILE_W
from ptx  import ptx_desc

import pprint
import sys

ARCADE_PAL  = "../original/GAME_DIR/AR1/STA/ARCADE.PAL"
TEXTS_IT    = "../original/GAME_DIR/PTX/Texts.kit"
ROOM_ROE    = "../original/GAME_DIR/AR1/MAP/ROOM.ROE"
BUFFER_MAT  = "../original/GAME_DIR/AR1/STA/BUFFER%X.MAT"
PTX         = "../original/GAME_DIR/AR1/FIL/PTX"

palette  = load_palette(ARCADE_PAL)
texts_it = parse_file(pti_desc, TEXTS_IT)
rooms    = parse_file(room_desc, ROOM_ROE)
hints    = parse_file(ptx_desc, PTX)

# TEXT
# ----

PTI_LINES = {}

def pti_file_to_dict():
    for block in texts_it['pti_blocks']:
        for line in block['lines']:
            n, l = line['line_id'], line['line']
            PTI_LINES[n] = l
pti_file_to_dict()

def print_text(i):
    print "%5d (%4x) - %s" % (i, i, PTI_LINES[i])

def print_all_text():
    for lines in sorted(PTI_LINES):
        print_text(lines)

# DRAW ROOMS
# ----------

def tile_getpixel(tile, x, y):
    return tile['rows'][y]['row'][x]['p']

def blit_tile(image, tile, dst_x, dst_y, flipped=False):
    for y in xrange(TILE_H):
        for x in xrange(TILE_W):
            if not flipped:
                image.put(dst_x + x,
                          dst_y + y,
                          tile_getpixel(tile, x, y))
            else:
                image.put(dst_x + TILE_W - x - 1,
                          dst_y + y,
                          tile_getpixel(tile, x, y))

ALL_MATS = {}

def get_mat(mat):
    if mat == 0:
        return None

    try:
        return ALL_MATS[mat]
    except KeyError:
        mat_file_name = BUFFER_MAT % mat
        ALL_MATS[mat] = parse_file(mat_desc, mat_file_name)

        return ALL_MATS[mat]

def show_room(room_nr):
    room = rooms['rooms'][room_nr]

    IMAGE_W = ROOM_W * TILE_W
    IMAGE_H = ROOM_H * TILE_H

    image = Image(IMAGE_W, IMAGE_H)
    for y in xrange(ROOM_H):
        for x in xrange(ROOM_W):
            tile_id    = room['tiles']     [y]['rows'][x]['tileid']
            tile_type  = room['tile_types'][y]['rows'][x]['tiletype']

            if tile_type != 0:
                print '%02x' % tile_type,
            else:
                print '  ',
            
            tile_nr = ((tile_id & 1) << 8) + (tile_id >>8)

            tile_mat = (tile_id & 0xf0) >> 4
            tile_mat = room['mat_files'][tile_mat]['file_number']

            flip = tile_id & 2

            the_mat = get_mat(tile_mat)
            if not the_mat:
                continue

            tile = the_mat['tiles'][tile_nr]

            if tile:
                blit_tile(image, tile, x * TILE_W, y * TILE_H, flip)

        print

    image.show(palette, mult=3)

# HINTS
# -----

def print_all_hints():
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
            print '    1.', PTI_LINES[pti1]
            print '    2.', PTI_LINES[pti2]

def print_hints():
    pass

# MAIN
# ----

def int_arg(func):
    def w(x):
        try:
            return func(int(x[0]))
        except IndexError:
            print 'one int arg, please'
        except ValueError:
            print 'one int arg, please'
    return w

def all_or_int(all_f, int_f):
    def w(rest):
        if len(rest) == 0:
            all_f()
        else:
            int_arg(int_f)(rest)
    return w

if __name__ == '__main__':
    commands = {
        'show_room': int_arg(show_room),
        'text': all_or_int(print_all_text, print_text),
        'hints': all_or_int(print_all_hints, print_hints),
    }

    if len(sys.argv) == 1:
        print 'Commands:'
        print ', '.join(commands.iterkeys())
        sys.exit(0)

    command, rest = sys.argv[1], sys.argv[2:]
    commands[command](rest)
