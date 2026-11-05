"""Verify the student commands in an isolated disposable copy of the kit."""
from pathlib import Path
import tempfile,shutil,json,subprocess
SOURCE=Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='soc-course-check-') as temp:
    root=Path(temp)/'SOC_Hands_On_Labs'
    shutil.copytree(SOURCE,root,ignore=shutil.ignore_patterns('work','__pycache__','capstone_aes.key'))
    (root/'work').mkdir()
    curriculum=json.loads((root/'instructor/curriculum.json').read_text())
    def run(command,expected=0):
        result=subprocess.run(['bash','-e','-c',command],cwd=root,text=True,capture_output=True)
        if (expected==0 and result.returncode!=0) or (expected!=0 and result.returncode==0):
            raise RuntimeError(command+'\n'+result.stdout+'\n'+result.stderr)
        return result
    for lesson in curriculum['lessons']:
        for i,step in enumerate(lesson['steps']):
            bad=(lesson['title']=='XOR-92' and i==2) or (lesson['title']=='AES-256-GCM' and i==3)
            run(step['command'],expected=1 if bad else 0)
        print('PASS',lesson['title'],'forward/reverse and applicable failure exercise')
    assert not (root/'work/aes_wrong.txt').exists()
    for name in ['cap_build','cap_recover','incident']:
        for step in curriculum[name]:run(step['command'])
        print('PASS',name,'all student commands')
    # Verify students can recover the artifact they built, with its own key pair.
    run('python3 labs/01_base64.py decode work/create/my_capstone.b64 work/capstone/envelope.json')
    run('python3 exercises/capstone.py extract')
    run('node labs/06_rsa.js decrypt work/capstone/wrapped_key.b64 work/capstone/aes.key keys/student_capstone.private.pem')
    for step in curriculum['cap_recover'][3:]:run(step['command'])
    print('PASS student-created capstone recovery')
    packet=json.loads((root/'work/aes.json').read_text())
    import base64
    changed=bytearray(base64.b64decode(packet['tag_b64']));changed[0]^=1
    packet['tag_b64']=base64.b64encode(changed).decode()
    (root/'work/tampered.json').write_text(json.dumps(packet))
    run('node labs/05_aes.js decrypt work/tampered.json work/tampered_plain.txt keys/practice_aes.key',expected=1)
    assert not (root/'work/tampered_plain.txt').exists()
    run('node labs/06_rsa.js decrypt work/rsa.b64 work/wrong_rsa.txt keys/incident.private.pem',expected=1)
    assert not (root/'work/wrong_rsa.txt').exists()
    print('PASS AES tag tamper rejection and RSA wrong-key rejection')
print('ALL COURSE CHECKS PASSED')
