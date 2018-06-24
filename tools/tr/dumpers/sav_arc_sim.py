from dumper import *

FILENAME = "../original/SAVEGAME/SAV0ARC1.SIM"

sav_arc_desc = (
    (string,  'header_tag',      { 'length': fixed(0x46), 'pascal': fixed(True) }),
    (uint16,  'pupo_x'),
    (uint16,  'pupo_y'),
    (uint8,   'counter_to_set_vita'),
    (uint8,   'current_room_number'),
    (uint8,   'wanted_room'),
    (uint8,   'read_from_usc_at_change_room'),
    (uint8,   'maybe_exit_related'),
    (uint8,   'boh1'),
    (uint8,   'gun_bool'),
    (uint8,   'colpi'),
    (uint8,   'current_ani'),
    (padding, 'pu', { 'size':   fixed(3920) }),
    (padding, 'pn', { 'size':   fixed(178) }),
    (array,   '100h_game_state', {
        'items_struct': (
            (uint8, 't'),
        ),
        'items': fixed(0x100),
    }),
    (uint16,  'vita'),
    (uint16,  'punti'),
    (uint8,   'faccia_countdown'),
    (uint8,   'boh2'),
    (uint8,   'punti_countdown'),
    (uint32,  'room_timer'),
    (uint8,   'boh3'),
    (uint8,   'boh4'),
    (uint32,  'boh5'),
    (uint16,  'to_set_pupo_x'),
    (uint16,  'to_set_pupo_y'),
)

