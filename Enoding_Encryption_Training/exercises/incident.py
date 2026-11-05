"""Extract supplied case evidence and verify recovered files. Never encrypts."""
from pathlib import Path
import argparse,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser();p.add_argument('action',choices=['extract','verify']);a=p.parse_args()
work=ROOT/'work/incident';work.mkdir(parents=True,exist_ok=True)
names=['invoice.txt','staff.csv','recovery-plan.txt']
if a.action=='extract':
    obj=json.loads((work/'bundle.json').read_text())
    if obj.get('format')!='SOC-INCIDENT-1':raise ValueError('Wrong case format')
    if [rec['name'] for rec in obj['records']]!=names:raise ValueError('Unexpected fixed case filenames')
    for rec in obj['records']:
        name=rec['name']
        (work/(name+'.wrapped.b64')).write_text(rec['wrapped_key_b64']+'\n')
        (work/(name+'.aes.json')).write_text(json.dumps(rec['aes_packet'],indent=2)+'\n')
    print('Extracted 3 AES packets and 3 RSA-wrapped keys. No decryption performed.')
else:
    baseline=json.loads((ROOT/'challenges/incident/baseline.json').read_text())
    for name in names:
        actual=hashlib.sha256((work/'recovered'/name).read_bytes()).hexdigest()
        if actual!=baseline[name]:raise SystemExit('FAIL: '+name)
        print('PASS',name,actual)
