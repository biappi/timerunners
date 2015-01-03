from imageutils import Image
from pal import load_palette

FILENAME = "../original/GAME_DIR/AR1/STA/BUFFER1.MAT"

def show_tileset(filename, palette):
    mat = file(filename, 'rb').read()

    tileset = Image(320, 200)
    tilewidth  = 16 
    tileheight = 10

    i = iter(ord(i) for i in mat)

    tiles = []

    for _ in xrange((320 / tilewidth)*(200 / tileheight)):
        rows = []
        tiles.append(rows)

        for y in xrange(tileheight):
            row = []
            rows.append(row)

            for x in xrange(tilewidth):
                row.append(next(i))


    for i, tile in enumerate(tiles):
        tile_x = i % (320/tilewidth)
        tile_y = i / (320/tilewidth)
        tile_x *= tilewidth
        tile_y *= tileheight

        for y, row in enumerate(tile):
            for x, pixel in enumerate(row):
                tileset.put(tile_x + x, tile_y + y, pixel)

    tileset.show(palette, mult=3)

pal_file = "../original/GAME_DIR/AR1/STA/ARCADE.PAL"
palette = load_palette(pal_file)

show_tileset('../original/GAME_DIR/AR1/STA/BUFFER1.MAT', palette)
show_tileset('../original/GAME_DIR/AR1/STA/BUFFER2.MAT', palette)
show_tileset('../original/GAME_DIR/AR1/STA/BUFFER3.MAT', palette)
show_tileset('../original/GAME_DIR/AR1/STA/BUFFER4.MAT', palette)
show_tileset('../original/GAME_DIR/AR1/STA/BUFFER5.MAT', palette)
show_tileset('../original/GAME_DIR/AR1/STA/BUFFER6.MAT', palette)
show_tileset('../original/GAME_DIR/AR1/STA/BUFFERA.MAT', palette)
show_tileset('../original/GAME_DIR/AR1/STA/BUFFERB.MAT', palette)

