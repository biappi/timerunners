function downloadFile(url) {
    return new Promise((resolve, reject) => {
        var request = new XMLHttpRequest();
        request.open("GET", url, true);
        request.responseType = "arraybuffer";
        request.onload = function (event) {
            var arrayBuffer = request.response;
            if (!arrayBuffer)
                reject();
            else
                resolve(new Uint8Array(arrayBuffer));
        };
        request.send(null);
    });
}
class Palette {
    constructor(data) {
        this.data = data;
    }
    color(index) {
        return {
            r: this.data[5 + index * 3] << 2,
            g: this.data[5 + index * 3 + 1] << 2,
            b: this.data[5 + index * 3 + 2] << 2,
        };
    }
}
ImageData.prototype.put = function (point, color) {
    var x = point.x;
    var y = point.y;
    this.data[((16 * y) + x) * 4] = color.r;
    this.data[((16 * y) + x) * 4 + 1] = color.g;
    this.data[((16 * y) + x) * 4 + 2] = color.b;
    this.data[((16 * y) + x) * 4 + 3] = 0xff;
};
CanvasRenderingContext2D.prototype.put_image_data = function (point, imagedata) {
    this.putImageData(imagedata, point.x, point.y);
};
function tile_index_to_position(tile_index) {
    return {
        x: (~~(tile_index % 20)) * 16,
        y: (~~(tile_index / 20)) * 10,
    };
}
function mat_content_to_image_data(pal, mat, offset, flip) {
    var tile = new ImageData(16, 10);
    for (var y = 0; y < 10; y++) {
        for (var x = 0; x < 16; x++) {
            let i = flip ? 16 - x : x;
            let color = mat[offset + y * 16 + i];
            tile.put({ x: x, y: y }, pal.color(color));
        }
    }
    return tile;
}
function map_content_to_tiles(mat, pal) {
    var tiles = [];
    for (var i = 0; i < mat.length / 160; i++) {
        tiles.push({
            normal: mat_content_to_image_data(pal, mat, 160 * i, false),
            flipped: mat_content_to_image_data(pal, mat, 160 * i, true),
        });
    }
    return tiles;
}
function create_image_element(imagedata) {
    let canvas = document.createElement("canvas");
    canvas.width = imagedata.width;
    canvas.height = imagedata.height;
    canvas.getContext("2d").putImageData(imagedata, 0, 0);
    return canvas;
}
function create_tileset_canvas() {
    let canvas = document.createElement("canvas");
    canvas.width = 320;
    canvas.height = 200;
    document.body.appendChild(canvas);
    return canvas;
}
function create_and_draw_tileset_canvas(tileset) {
    let p = create_tileset_canvas();
    let ctx = p.getContext("2d");
    for (var i = 0; i < tileset.length; i++) {
        ctx.put_image_data(tile_index_to_position(i), tileset[i]);
    }
}
class Room {
    constructor(data, nr) {
        this.data = data;
        this.nr = nr;
    }
    static sizeof() { return 0x4f4; }
    offset() { return Room.sizeof() * this.nr; }
    tilemap_at(index) {
        return (this.data[this.offset() + 0x04 + index * 2 + 1]);
    }
    tileid_at(index) {
        return ((this.data[this.offset() + 0x24 + index * 2] << 8) +
            (this.data[this.offset() + 0x24 + index * 2 + 1] << 0));
    }
}
function parse_room(roomdata) {
    let rooms = [];
    for (let nr = 0; nr < roomdata.length / Room.sizeof(); nr++)
        rooms.push(new Room(roomdata, nr));
    return rooms;
}
function draw_room(room, tilesets, ctx) {
    ctx.fillStyle = 'magenta';
    ctx.fillRect(0, 0, 320, 200);
    for (var i = 0; i < 0x14 * 0x14; i++) {
        let tile_id = room.tileid_at(i);
        let flip = !!(tile_id & 0x0200);
        let tile_nr = (tile_id & 0x0fff) & 0x1ff;
        let tileset_id = (tile_id & 0xf000) >> 12;
        let tileset_nr = room.tilemap_at(tileset_id);
        let tileset = tilesets.get(tileset_nr);
        if (!tileset)
            continue;
        let tile = tileset[tile_nr];
        if (!tile) {
            console.log(tile_nr);
            continue;
        }
        let point = tile_index_to_position(i);
        room_ctx.put_image_data(point, flip ? tile.flipped : tile.normal);
    }
}
function css_px(value, multiplier) {
    return "" + (value * multiplier) + "px";
}
var next_room = () => { };
var prev_room = () => { };
var draw_current_room = () => { };
document.write("<h1>TR</h1>");
let flex_container = document.createElement("div");
flex_container.style.display = "flex";
let room_div = document.createElement("div");
room_div.id = "room";
room_div.style.position = "relative";
room_div.style.width = "" + (320 * 3) + "px";
let room_title = document.createElement("div");
room_div.appendChild(room_title);
flex_container.appendChild(room_div);
let canvas_container = document.createElement("div");
canvas_container.style.position = "relative";
room_div.appendChild(canvas_container);
let room_canvas = document.createElement("canvas");
room_canvas.width = 320;
room_canvas.height = 200;
room_canvas.style.width = "" + (room_canvas.width * 3) + "px";
room_canvas.style.height = "" + (room_canvas.height * 3) + "px";
canvas_container.appendChild(room_canvas);
let room_bottom = document.createElement("div");
room_div.appendChild(room_bottom);
let tilesets_div = document.createElement("div");
tilesets_div.id = "tilesets";
tilesets_div.style.width = "640px";
tilesets_div.style.minWidth = "640px";
tilesets_div.style.height = "100%";
tilesets_div.style.overflow = "scroll";
flex_container.appendChild(tilesets_div);
let room_ctx = room_canvas.getContext("2d");
document.getElementsByTagName("body")[0].appendChild(flex_container);
window.onload = () => {
    Promise.all([
        downloadFile("tr/GAME_DIR/AR1/STA/ARCADE.PAL"),
        Promise.all([1, 2, 3, 4, 5, 6, 0xa, 0xb].map((nr) => {
            let x = '0123456789ABCDEF'[nr];
            return downloadFile("tr/GAME_DIR/AR1/STA/BUFFER" + x + ".MAT")
                .then((data) => { return { nr: nr, data: data }; });
        })),
        downloadFile("tr/GAME_DIR/AR1/MAP/ROOM.ROE").then((file) => { return parse_room(file); })
    ])
        .then((files) => {
        let palette = new Palette(files[0]);
        let buffers = files[1];
        let rooms = files[2];
        let tilesets_tuples = buffers.map((tileset) => {
            return [tileset.nr, map_content_to_tiles(tileset.data, palette)];
        });
        let tilesets = new Map(tilesets_tuples);
        tilesets.forEach((tileset, nr) => {
            let tileset_title = document.createElement("div");
            tileset_title.innerHTML = "<h3>Tileset " + nr + "<h3>";
            tilesets_div.appendChild(tileset_title);
            tileset.forEach((tile) => {
                let element = create_image_element(tile.normal);
                element.style.width = "" + (element.width * 2) + "px";
                element.style.height = "" + (element.height * 2) + "px";
                tilesets_div.appendChild(element);
            });
        });
        var current_room = 0;
        next_room = () => {
            current_room += 1;
            draw_current_room();
        };
        prev_room = () => {
            current_room -= 1;
            draw_current_room();
        };
        draw_current_room = () => {
            room_title.innerHTML = "<a href='#' onclick='javascript:prev_room()'>prev</a> • <h3 style='display: inline'>Room nr. " + current_room + "</h3> • <a href='#' onclick='javascript:next_room()'>next</a>";
            draw_room(rooms[current_room], tilesets, room_ctx);
        };
        draw_current_room();
        var pointer_div = document.createElement("div");
        pointer_div.style.position = "absolute";
        pointer_div.style.visibility = "hidden";
        pointer_div.style.background = "rgba(255,255,255,0.4)";
        pointer_div.style.width = css_px(16, 3);
        pointer_div.style.height = css_px(10, 3);
        canvas_container.appendChild(pointer_div);
        canvas_container.onmouseenter = () => {
            pointer_div.style.visibility = "visible";
        };
        canvas_container.onmouseleave = () => {
            pointer_div.style.visibility = "hidden";
            console.log("leave");
        };
        canvas_container.onmousemove = (ev) => {
            let bounds = ev.target.getBoundingClientRect();
            let mousePoint = {
                x: Math.floor((ev.clientX - bounds.left) / 3),
                y: Math.floor((ev.clientY - bounds.top) / 3),
            };
            let mouseTile = {
                x: Math.floor(mousePoint.x / 0x14),
                y: Math.floor(mousePoint.y / 0x14),
            };
            pointer_div.style.left = css_px(mousePoint.x, 3);
            pointer_div.style.top = css_px(mousePoint.y, 3);
            room_bottom.innerHTML = ("Mouse: " + JSON.stringify(mousePoint) + "<br>"
                + "tile: " + JSON.stringify(mouseTile) + "<br>");
        };
    });
};
