"""Package/extract existing layers. This script does not decrypt anything."""
from pathlib import Path
import argparse,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser()
p.add_argument('action',choices=['package','extract','verify'])
p.add_argument('--envelope',default='work/capstone/envelope.json')
p.add_argument('--directory',default='work/capstone')
p.add_argument('--payload',default='work/capstone/recovered.js')
a=p.parse_args()
def local(name):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT):raise ValueError('Use local exercise paths')
    return path
d=local(a.directory)
if not d.is_relative_to(ROOT/'work'):raise ValueError('Directory must be under work/')
d.mkdir(parents=True,exist_ok=True)
if a.action=='package':
    packet=json.loads((d/'aes.json').read_text())
    envelope={'format':'SOC-CAPSTONE-1','key_wrap':'RSA-OAEP-SHA256','wrapped_key_b64':(d/'wrapped_key.b64').read_text().strip(),'aes_packet':packet}
    local(a.envelope).write_text(json.dumps(envelope,indent=2)+'\n')
    print('Packaged already-created layers. Next, Base64-encode the envelope.')
elif a.action=='extract':
    obj=json.loads(local(a.envelope).read_text())
    if obj.get('format')!='SOC-CAPSTONE-1':raise ValueError('Wrong capstone format')
    (d/'wrapped_key.b64').write_text(obj['wrapped_key_b64']+'\n')
    (d/'aes.json').write_text(json.dumps(obj['aes_packet'],indent=2)+'\n')
    print('Extracted wrapped AES key and AES packet. No decryption performed.')
else:
    original=(ROOT/'inputs/capstone_payload.js').read_bytes()
    actual=local(a.payload).read_bytes()
    if actual!=original:raise SystemExit('FAIL: bytes differ')
    print('PASS: recovered payload matches original. SHA-256:',hashlib.sha256(actual).hexdigest())
