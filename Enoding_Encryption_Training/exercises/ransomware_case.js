'use strict';
// Fixed synthetic case generator. No directory enumeration or user-file encryption.
const {crypto,read,write,encrypt,oaep}=require('../labs/common');
const action=process.argv[2];
const samples={
 'invoice.txt':Buffer.from('TRAINING INVOICE\nCustomer: Example Company\nAmount: 125.00 USD\n'),
 'staff.csv':Buffer.from('name,team\nAlex,SOC\nMorgan,DFIR\n'),
 'recovery-plan.txt':Buffer.from('TRAINING RECOVERY PLAN\nValidate recovery using known-good hashes.\n')
};
if(action==='create'){
 const publicKey=read('keys/incident.public.pem');
 const records=Object.entries(samples).map(([name,bytes])=>{
  const key=crypto.randomBytes(32);
  return {name,wrapped_key_b64:crypto.publicEncrypt({key:publicKey,...oaep},key).toString('base64'),aes_packet:encrypt(bytes,key)};
 });
 const bundle={format:'SOC-INCIDENT-1',description:'Synthetic ransomware recovery evidence',records};
 write('challenges/incident/bundle.lab.b64',Buffer.from(JSON.stringify(bundle)).toString('base64')+'\n');
 const baseline=Object.fromEntries(Object.entries(samples).map(([name,bytes])=>[name,crypto.createHash('sha256').update(bytes).digest('hex')]));
 write('challenges/incident/baseline.json',JSON.stringify(baseline,null,2)+'\n');
 write('challenges/incident/READ_ME_TRAINING.txt','TRAINING ONLY: Synthetic case. Documents appear inaccessible. Supplied keys enable recovery. No ransom demand or actual compromise.\n');
 write('challenges/incident/events.csv','time,host,process,event,detail\n09:00:00,LAB-WS1,training-fixture,process_start,SYNTHETIC event sequence\n09:00:01,LAB-WS1,training-fixture,encrypted_copy,invoice.txt\n09:00:02,LAB-WS1,training-fixture,encrypted_copy,staff.csv\n09:00:03,LAB-WS1,training-fixture,encrypted_copy,recovery-plan.txt\n09:00:04,LAB-WS1,training-fixture,note_present,READ_ME_TRAINING.txt\n');
 console.log('Created fixed in-memory training evidence. No existing documents were encrypted.');
}else{
 console.error('Usage: node exercises/ransomware_case.js create');process.exitCode=1;
}
