'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const ROOT = path.resolve(__dirname, '..');
function local(name) {
  const p = path.resolve(ROOT, name);
  if (p !== ROOT && !p.startsWith(ROOT + path.sep)) throw Error('Use paths within this training folder');
  return p;
}
function read(name) { return fs.readFileSync(local(name)); }
function write(name, data, secret = false) {
  const p = local(name), relative = path.relative(ROOT, p);
  if (!['work','keys','challenges'].includes(relative.split(path.sep)[0])) throw Error('Outputs belong under work/, keys/, or challenges/');
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, data, { mode: secret ? 0o600 : 0o644 });
  if (secret) fs.chmodSync(p, 0o600);
  console.log('Saved', relative);
}
function encrypt(data, key) {
  if(key.length!==32) throw Error('AES key must contain exactly 32 bytes');
  const nonce=crypto.randomBytes(12);
  const cipher=crypto.createCipheriv('aes-256-gcm',key,nonce);
  const ciphertext=Buffer.concat([cipher.update(data),cipher.final()]);
  return {algorithm:'aes-256-gcm',nonce_b64:nonce.toString('base64'),tag_b64:cipher.getAuthTag().toString('base64'),ciphertext_b64:ciphertext.toString('base64')};
}
function decrypt(packet,key) {
  if(packet.algorithm!=='aes-256-gcm'||key.length!==32) throw Error('Wrong algorithm or key length');
  const dec=crypto.createDecipheriv(packet.algorithm,key,Buffer.from(packet.nonce_b64,'base64'));
  dec.setAuthTag(Buffer.from(packet.tag_b64,'base64'));
  // Keep update() output private until final() authenticates it.
  return Buffer.concat([dec.update(Buffer.from(packet.ciphertext_b64,'base64')),dec.final()]);
}
const oaep={padding:crypto.constants.RSA_PKCS1_OAEP_PADDING,oaepHash:'sha256'};
module.exports={fs,path,crypto,ROOT,local,read,write,encrypt,decrypt,oaep};
