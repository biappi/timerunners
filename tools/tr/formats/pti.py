from tr import dumpers

def pti_file_to_dict(text_file):
    lines = {}

    for block in text_file['pti_blocks']:
        for line in block['lines']:
            n, l = line['line_id'], line['line']
            lines[n] = l

    return lines

def main(args):
    try: filename = args[1]
    except: filename = dumpers.pti.FILENAME

    texts = dumpers.parse_file(dumpers.pti.desc, filename)
    lines = pti_file_to_dict(texts)

    for i in sorted(lines):
        print "%5d (%4x) - %s" % (i, i, lines[i])
