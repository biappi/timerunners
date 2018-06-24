from tr import formats

import sys

try:    formatname = sys.argv[1]
except: formatname = None

try:    filename = sys.argv[2]
except: filename = None

if formatname is None:
    print "available formats"
    for name in formats.all_formats:
        print '    ' + name
else:
    fileformat = getattr(formats, formatname, None)
    if fileformat is None:
        print "No format named:", formatname
        sys.exit(1)

    fileformat.main(sys.argv)
