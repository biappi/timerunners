from tr import dumpers
from tr.dumpers.room import ROOM_W, ROOM_H
from tr.dumpers.mat import TILE_H, TILE_W

from ..utils.imageutils import Image
from pal  import load_palette

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

def image_for_room(room, tilemaps):
    IMAGE_W = ROOM_W * TILE_W
    IMAGE_H = ROOM_H * TILE_H

    image = Image(IMAGE_W, IMAGE_H)
    for y in xrange(ROOM_H):
        for x in xrange(ROOM_W):
            tile_id    = room['tiles']     [y]['rows'][x]['tileid']
            tile_type  = room['tile_types'][y]['rows'][x]['tiletype']

            tile_nr = ((tile_id & 1) << 8) + (tile_id >>8)

            tile_mat = (tile_id & 0xf0) >> 4
            tile_mat = room['mat_files'][tile_mat]['file_number']

            flip = tile_id & 2

            if tile_mat >= len(tilemaps):
                continue

            the_mat = tilemaps[tile_mat]
            if not the_mat:
                continue

            if tile_nr >= len(the_mat['tiles']):
                continue

            tile = the_mat['tiles'][tile_nr]
            if not tile:
                continue

            blit_tile(image, tile, x * TILE_W, y * TILE_H, flip)

    return image

def load_tilemap(i):
    try:
        BUFFER_MAT  = "../original/GAME_DIR/AR1/STA/BUFFER%X.MAT"
        mat_file_name = BUFFER_MAT % i
        return dumpers.parse_file(dumpers.mat.desc, mat_file_name)
    except:
        return None

def load_tilemaps():
    return [load_tilemap(i) for i in xrange(0xc)]

def main(args):
    try:    room_nr = int(args[2])
    except: room_nr = 0

    ARCADE_PAL  = "../original/GAME_DIR/AR1/STA/ARCADE.PAL"
    ROOM_ROE    = "../original/GAME_DIR/AR1/MAP/ROOM.ROE"

    palette  = load_palette(ARCADE_PAL)
    tilemaps = load_tilemaps()
    rooms    = dumpers.parse_file(dumpers.room.desc, ROOM_ROE)
    room     = rooms['rooms'][room_nr]

    image = image_for_room(room, tilemaps)
    image.show(palette, mult=3)

