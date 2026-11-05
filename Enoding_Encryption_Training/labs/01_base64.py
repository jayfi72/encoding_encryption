import argparse
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def local(name):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('Keep exercise paths within this training folder')
    return path

def save(name, data):
    path = local(name)
    if not path.is_relative_to(ROOT / 'work'):
        raise ValueError('Write practice results under work/')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    print('Saved', path.relative_to(ROOT), '-', len(data), 'bytes')

import base64
p = argparse.ArgumentParser(description='Base64 representation, no secret key')
p.add_argument('action', choices=['encode', 'decode'])
p.add_argument('input'); p.add_argument('output')
a = p.parse_args()
data = local(a.input).read_bytes()
if a.action == 'encode':
    result = base64.b64encode(data) + b'\n'
else:
    result = base64.b64decode(b''.join(data.split()), validate=True)
save(a.output, result)
