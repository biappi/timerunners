from dumper import *

FILENAME = "../original/MANAGER.PAL"
FILENAME = "../original/GAME_DIR/AR1/STA/ARCADE.PAL"

desc = (
    (uint8,   'first_color'),
    (uint8,   'count'),
    (padding, 'unused', {'size': fixed(2) }),
    (uint8,   'must_be_80'),
    (array,   'palette', {
        'items_struct': (
            (uint8, 'r'),
            (uint8, 'g'),
            (uint8, 'b'),
        ),
        'items_including': relative('.count'),
    }),
)


