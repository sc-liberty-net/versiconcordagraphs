"""concordagraph.html is CRLF. A patch written with LF newlines matches nothing
multi-line, and inserting LF text into a CRLF file leaves mixed endings. Convert
every text field of the patch before applying.
"""
import json, io, sys

src, dst = sys.argv[1], sys.argv[2]
ops = json.load(io.open(src, encoding='utf-8'))

FIELDS = ('old', 'new', 'after', 'before', 'insert')
n = 0
for op in ops:
    for f in FIELDS:
        if f in op and isinstance(op[f], str):
            before = op[f]
            op[f] = before.replace('\r\n', '\n').replace('\n', '\r\n')
            if op[f] != before:
                n += 1

io.open(dst, 'w', encoding='utf-8', newline='').write(
    json.dumps(ops, ensure_ascii=False, indent=1))
print('converted %d field(s) across %d op(s) -> %s' % (n, len(ops), dst))
