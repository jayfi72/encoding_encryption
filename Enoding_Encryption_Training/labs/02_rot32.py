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

p = argparse.ArgumentParser(description='ASCII letter rotation by 32 modulo 26')
p.add_argument('action', choices=['encode', 'decode'])
p.add_argument('input'); p.add_argument('output')
a = p.parse_args()
shift = 32 if a.action == 'encode' else -32
def rotate(byte):
    if 65 <= byte <= 90: return 65 + (byte - 65 + shift) % 26
    if 97 <= byte <= 122: return 97 + (byte - 97 + shift) % 26
    return byte
save(a.output, bytes(rotate(b) for b in local(a.input).read_bytes()))
