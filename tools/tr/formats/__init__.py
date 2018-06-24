import ani
import chv
import ele
import i16
import ins
import mat
import pal
import pla
import pti
import ptx
import room

all_formats = dir()
all_formats = filter(lambda i: not i.startswith('__'), all_formats)
all_formats = filter(lambda i: getattr(globals()[i], 'main', None) is not None, all_formats)

