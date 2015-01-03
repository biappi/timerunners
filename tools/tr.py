from dumper import parse_file
from imageutils import Image

from pal import load_palette
from room import room_desc, ROOM_W, ROOM_H
from mat import mat_desc, TILE_H, TILE_W

import pprint
import sys

ARCADE_PAL  = "../original/GAME_DIR/AR1/STA/ARCADE.PAL"

ROOM_ROE    = "../original/GAME_DIR/AR1/MAP/ROOM.ROE"
BUFFER_MAT  = "../original/GAME_DIR/AR1/STA/BUFFER%X.MAT"

palette = load_palette(ARCADE_PAL)
rooms   = parse_file(room_desc, ROOM_ROE)

# = #

room = rooms['rooms'][7]

IMAGE_W = ROOM_W * TILE_W
IMAGE_H = ROOM_H * TILE_H

print TILE_W, TILE_H
print ROOM_W, ROOM_H
print IMAGE_W, IMAGE_H

def tile_getpixel(tile, x, y):
    return tile['rows'][y]['row'][x]['p']

image = Image(IMAGE_W, IMAGE_H)
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

for y in xrange(ROOM_H):
    for x in xrange(ROOM_W):
        tile_id  = room['tiles'][y]['rows'][x]['tileid']

        #print '%02x' % tile_nr,
        
        tile_nr = ((tile_id & 1) << 8) + (tile_id >>8)

        tile_mat = (tile_id & 0xf0) >> 4
        tile_mat = room['mat_files'][tile_mat]['file_number']

        flip = tile_id & 2

        #print "%04x" % tile_id,

        the_mat = get_mat(tile_mat)
        if not the_mat:
            continue

        tile = the_mat['tiles'][tile_nr]

        if tile:
            blit_tile(image, tile, x * TILE_W, y * TILE_H, flip)

    #print

image.show(palette, mult=3)
