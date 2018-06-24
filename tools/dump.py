from tr import dumpers
from tr import formats

import sys

try:    dumpername = sys.argv[1]
except: dumpername = None

try:    filename = sys.argv[2]
except: filename = None

if dumpername is None:
    print "available dumpers"
    for name, example_file in dumpers.dumpers_examples:
        print ('  * ' if example_file else '    ')  + name
else:
    dumper = getattr(dumpers, dumpername, None)
    if dumper is None:
        print "No dumper named:", dumpername
        sys.exit(1)

    if filename is None:
        filename = dict(dumpers.dumpers_examples).get(dumpername, None)

    if filename is None:
        print "No filename specified and no defaults for dumper:", dumpername
        sys.exit(1)

        
    dumpers.dumper.dump_file(dumper.desc, filename)

