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

import gzip, io
p = argparse.ArgumentParser(description='gzip compression and decompression')
p.add_argument('action', choices=['compress', 'decompress'])
p.add_argument('input'); p.add_argument('output')
a = p.parse_args()
data = local(a.input).read_bytes()
if a.action == 'compress': result = gzip.compress(data, mtime=0)
else:
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
        result = stream.read(4 * 1024 * 1024 + 1)
    if len(result) > 4 * 1024 * 1024:
        raise ValueError('Exercise decompression limit is 4 MiB')
save(a.output, result)
