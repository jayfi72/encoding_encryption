'use strict';
const {fs,crypto,local,read,write,encrypt,decrypt}=require('./common');
const [action,input,output,keyfile]=process.argv.slice(2);
if(action==='keygen'&&input){
  if(fs.existsSync(local(input))) throw Error('Key exists. Reuse it or choose a new key filename.');
  write(input,crypto.randomBytes(32),true);
}else if(action==='encrypt'&&keyfile){
  write(output,JSON.stringify(encrypt(read(input),read(keyfile)),null,2)+'\n');
}else if(action==='decrypt'&&keyfile){
  write(output,decrypt(JSON.parse(read(input).toString('utf8')),read(keyfile)));
}else{
  console.error('Usage: node labs/05_aes.js keygen keys/NAME.key\n       node labs/05_aes.js encrypt|decrypt INPUT OUTPUT KEYFILE');
  process.exitCode=1;
}
