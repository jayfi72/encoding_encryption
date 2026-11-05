'use strict';
const {fs,crypto,local,read,write,oaep}=require('./common');
const [action,input,output,keyfile]=process.argv.slice(2);
if(action==='keygen'&&input){
  if(fs.existsSync(local(input+'.public.pem'))||fs.existsSync(local(input+'.private.pem'))) throw Error('Key pair exists. Reuse it or choose a new prefix.');
  const keys=crypto.generateKeyPairSync('rsa',{modulusLength:2048,publicKeyEncoding:{type:'spki',format:'pem'},privateKeyEncoding:{type:'pkcs8',format:'pem'}});
  write(input+'.public.pem',keys.publicKey);
  write(input+'.private.pem',keys.privateKey,true);
}else if(action==='encrypt'&&keyfile){
  const data=read(input);
  if(data.length>190) throw Error('RSA-2048 OAEP SHA-256 accepts at most 190 bytes. Encrypt a short message or AES key.');
  const encrypted=crypto.publicEncrypt({key:read(keyfile),...oaep},data);
  write(output,encrypted.toString('base64')+'\n');
}else if(action==='decrypt'&&keyfile){
  const ciphertext=Buffer.from(read(input).toString('utf8').trim(),'base64');
  write(output,crypto.privateDecrypt({key:read(keyfile),...oaep},ciphertext));
}else{
  console.error('Usage: node labs/06_rsa.js keygen keys/PREFIX\n       node labs/06_rsa.js encrypt|decrypt INPUT OUTPUT KEYFILE');
  process.exitCode=1;
}
