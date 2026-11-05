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

p = argparse.ArgumentParser(description='Single-byte XOR, a weak reversible cipher')
p.add_argument('action', choices=['encode', 'decode'])
p.add_argument('input'); p.add_argument('output')
p.add_argument('--key', type=int, required=True, help='Decimal byte value, e.g. 92')
a = p.parse_args()
if not 0 <= a.key <= 255: raise ValueError('Key must be from 0 to 255')
# XOR reverses itself, so encode and decode use the same byte operation.
save(a.output, bytes(byte ^ a.key for byte in local(a.input).read_bytes()))
