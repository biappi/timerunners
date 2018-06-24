import ani
import animjoytab
import chv
import dumper
import ele
import framestab
import i16
import ini
import ins
import logitab
import mat
import pal
import pn
import prt
import pti
import ptx
import pu
import room
import sav_arc_sim
import sav_mng_sim
import usc

from dumper import parse_file

all_dumpers = dir()
all_dumpers = filter(lambda i: not i.startswith('__'), all_dumpers)
all_dumpers = filter(lambda i: getattr(globals()[i], 'desc', None) is not None, all_dumpers)

_all_examples = (getattr(globals()[i], 'FILENAME', None) for i in all_dumpers)

dumpers_examples = zip(all_dumpers, _all_examples)
