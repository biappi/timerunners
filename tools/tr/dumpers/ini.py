from dumper import *

desc = (
    (uint16_be, 'boh1'),
    (uint16_be, 'boh2'),
    (uint32_be, 'boh3'),
    (uint16_be, 'pupo_palette_delta'),
    (uint16_be, 'current_room_nr'),
    (uint16_be, 'pupo_x'),
    (uint16_be, 'pupo_y'),
    (uint16_be, 'colpi'),
    (uint16_be, 'counter_to_set_vita'),
)
