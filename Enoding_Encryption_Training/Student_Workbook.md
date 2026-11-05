# SOC hands-on obfuscation and encryption course


Students perform each forward and reverse operation as separate commands. This kit replaces the earlier demonstration-only approach. Allow about three hours plus additional practice, or split across two sessions.


## Setup

Extract this folder on Ubuntu. Open a terminal in `SOC_Hands_On_Labs`. Python 3 and Node.js must already be installed. No npm/pip packages or outbound connection are needed during exercises. Run key-generation steps once. If a key exists, reuse it or choose a new filename; do not replace a key while retaining its old ciphertext.


```bash
python3 --version
node --version
pwd
ls labs inputs challenges
```

The six input files are under `inputs/`. Each routine has its own practice script and supplied source file. You can edit each input to personalize the exercise. Store results under `work/`.


## Command conventions

`python3` and `node` name the interpreter. The next word is the supplied practice file. `encode/decode`, `compress/decompress`, and `encrypt/decrypt` choose one direction. Positional arguments identify INPUT, OUTPUT, then KEYFILE for AES/RSA. `--key 92` supplies the decimal XOR byte. `cat` prints text, `od` prints bytes, `cmp` compares exact files, and `>` writes stdout to a file.


All source and recovered code remains data during these exercises. The scripts support transformation and inspection, not executing recovered JavaScript.


## Lab 1: Base64

An encoding represents bytes as text using a public 64-symbol alphabet. It provides no secret-key protection.

**Tool:** Python 3 base64 library. Ubuntu base64 provides an alternative.



### 1. Inspect your input

Read the supplied plain-text practice file. You may edit its message.

```bash
cat inputs/01_base64.txt
```

**Expected:** Base64 represents bytes as text.



### 2. Encode your file

encode converts source bytes into Base64 text. It does not encrypt them.

```bash
python3 labs/01_base64.py encode inputs/01_base64.txt work/base64.txt
cat work/base64.txt
```

**Expected:** A Base64 string that differs from the original message.



### 3. Decode your output

decode reverses the Base64 representation. This is a separate command.

```bash
python3 labs/01_base64.py decode work/base64.txt work/base64_recovered.txt
cat work/base64_recovered.txt
```

**Expected:** The original message returns.



### 4. Verify and try the native tool

cmp prints nothing when files match. --decode is the Ubuntu base64 reversal flag.

```bash
cmp inputs/01_base64.txt work/base64_recovered.txt
base64 --decode work/base64.txt > work/base64_native.txt
cmp inputs/01_base64.txt work/base64_native.txt
```

**Expected:** Both comparisons are silent and return status 0.



**Student checkpoint:** Explain why no secret key was needed. Change the input and repeat both directions.



## Lab 2: ROT32

A rotation cipher substitutes letters using an alphabet and shift. Here ASCII letters rotate by 32 modulo 26, equivalent to ROT6. This definition preserves case, digits and punctuation.

**Tool:** Python 3 byte translation. ROT32 here is explicitly a 26-letter Caesar rotation.



### 1. Inspect and encode

The forward operation shifts each letter by +32, equivalent to +6.

```bash
cat inputs/02_rot32.txt
python3 labs/02_rot32.py encode inputs/02_rot32.txt work/rot32.txt
cat work/rot32.txt
```

**Expected:** SOC becomes YUI. Digits 123 remain unchanged.



### 2. Reverse the rotation

The reverse operation shifts by -32. Applying +32 twice would not reverse it.

```bash
python3 labs/02_rot32.py decode work/rot32.txt work/rot32_recovered.txt
cat work/rot32_recovered.txt
```

**Expected:** The original sentence returns.



### 3. Verify the recovered bytes

The entire file, including case and punctuation, must match.

```bash
cmp inputs/02_rot32.txt work/rot32_recovered.txt
```

**Expected:** No output means a byte-for-byte match.



**Student checkpoint:** Predict one letter substitution and explain why 32 wraps to 6.



## Lab 3: gzip

gzip is a compression format. Compression reduces redundancy and decompression reconstructs the original bytes. No secret key is involved.

**Tool:** Python 3 gzip library. The gzip CLI can also decompress this exercise.



### 1. Compress your file

compress creates a gzip stream. od shows its first three bytes in hexadecimal.

```bash
python3 labs/03_gzip.py compress inputs/03_gzip.txt work/message.gz
od -An -tx1 -N 3 work/message.gz
```

**Expected:** Header bytes: 1f 8b 08.



### 2. Decompress your file

decompress reverses compression, with a 4 MiB output limit in this lab.

```bash
python3 labs/03_gzip.py decompress work/message.gz work/gzip_recovered.txt
cat work/gzip_recovered.txt
```

**Expected:** The repeated source sentence returns.



### 3. Verify and use the native tool

gzip -d decompresses and -c writes to stdout. Redirection saves it to a file.

```bash
cmp inputs/03_gzip.txt work/gzip_recovered.txt
gzip -dc work/message.gz > work/gzip_native.txt
cmp inputs/03_gzip.txt work/gzip_native.txt
```

**Expected:** Both recovered files match the original.



**Student checkpoint:** Explain why opaque compressed bytes do not prove encryption.



## Lab 4: XOR-92

XOR compares bits and returns 1 where they differ. Repeating XOR with the same byte key reverses it. A single repeated byte key is weak obfuscation, with 256 possibilities.

**Tool:** Python 3 bytewise ^ operator. Key 92 is decimal and equals hexadecimal 0x5c.



### 1. Apply XOR to your file

--key 92 supplies a decimal byte. Each input byte combines with that value.

```bash
python3 labs/04_xor.py encode inputs/04_xor.txt work/xor.bin --key 92
od -An -tx1 -N 16 work/xor.bin
```

**Expected:** The output bytes differ from the original text.



### 2. Reverse XOR with the same key

The ^ operation is identical in both directions. (P XOR K) XOR K equals P.

```bash
python3 labs/04_xor.py decode work/xor.bin work/xor_recovered.txt --key 92
cat work/xor_recovered.txt
```

**Expected:** The original practice sentence returns.



### 3. Compare correct and incorrect keys

XOR has no authentication tag. A wrong key can still produce output, so compare bytes.

```bash
cmp inputs/04_xor.txt work/xor_recovered.txt
python3 labs/04_xor.py decode work/xor.bin work/xor_wrong.txt --key 93
cmp inputs/04_xor.txt work/xor_wrong.txt
```

**Expected:** First comparison matches. Second reports a difference and status 1.



**Student checkpoint:** Explain why wrong-key XOR output can exist while AES-GCM rejects it.



## Lab 5: AES-256-GCM

AES means Advanced Encryption Standard. It is symmetric: the same secret key enables encryption and decryption. Galois/Counter Mode adds authentication. This lab uses a 32-byte key, fresh 12-byte nonce and authentication tag.

**Tool:** Node.js built-in node:crypto library. No npm package is required.



### 1. Generate your secret key

keygen creates 32 random bytes. Run this once, then retain the key.

```bash
node labs/05_aes.js keygen keys/practice_aes.key
```

**Expected:** A teaching key at keys/practice_aes.key.



### 2. Encrypt your practice file

encrypt creates a fresh nonce and tag. Binary fields use Base64 for JSON storage.

```bash
node labs/05_aes.js encrypt inputs/05_aes.txt work/aes.json keys/practice_aes.key
cat work/aes.json
```

**Expected:** A packet with algorithm, nonce_b64, tag_b64 and ciphertext_b64. It does not contain the key.



### 3. Decrypt using your key

decrypt decodes the packet fields, uses the secret key, and verifies the GCM tag before writing output.

```bash
node labs/05_aes.js decrypt work/aes.json work/aes_recovered.txt keys/practice_aes.key
cat work/aes_recovered.txt
```

**Expected:** The original practice sentence returns.



### 4. Verify, then test a wrong key

Use a different generated key. The final command must fail authentication.

```bash
cmp inputs/05_aes.txt work/aes_recovered.txt
node labs/05_aes.js keygen keys/wrong_aes.key
node labs/05_aes.js decrypt work/aes.json work/aes_wrong.txt keys/wrong_aes.key
```

**Expected:** Comparison matches. Wrong-key command exits nonzero and writes no new plaintext file.



**Student checkpoint:** Identify the key, nonce, ciphertext and tag. Explain why Base64 decoding alone cannot recover the message.



## Lab 6: RSA-OAEP

RSA, named for Rivest, Shamir and Adleman, is asymmetric. For confidentiality, the public key encrypts and the matching private key decrypts. OAEP is Optimal Asymmetric Encryption Padding. This lab uses RSA-2048 and SHA-256.

**Tool:** Node.js built-in node:crypto library. RSA here protects short messages or AES keys.



### 1. Generate your key pair

keygen creates a public PEM and a private PEM. Retain the matching pair.

```bash
node labs/06_rsa.js keygen keys/practice_rsa
```

**Expected:** keys/practice_rsa.public.pem and keys/practice_rsa.private.pem.



### 2. Encrypt your short message

The public key encrypts the input using OAEP-SHA256. Output uses Base64.

```bash
node labs/06_rsa.js encrypt inputs/06_rsa.txt work/rsa.b64 keys/practice_rsa.public.pem
cat work/rsa.b64
```

**Expected:** A Base64 representation of RSA ciphertext. Values vary each run.



### 3. Decrypt with the private key

The matching private key reverses RSA encryption using the same OAEP parameters.

```bash
node labs/06_rsa.js decrypt work/rsa.b64 work/rsa_recovered.txt keys/practice_rsa.private.pem
cat work/rsa_recovered.txt
```

**Expected:** The short practice message returns.



### 4. Verify the recovered message

A Base64-wrapped public key is still a public key. Decoding it does not create a private key.

```bash
cmp inputs/06_rsa.txt work/rsa_recovered.txt
```

**Expected:** No output means success. This RSA configuration accepts at most 190 input bytes.



**Student checkpoint:** Explain why RSA wraps the 32-byte AES key in the capstone instead of the entire payload.



## Capstone: build one file using all six routines

Create in this order: ROT32, XOR-92, gzip, AES-GCM, RSA-wrap the AES key, then package and Base64-encode. RSA protects the key rather than bulk data. The resulting single artifact contains ciphertext and a wrapped key. The private key stays separate.


### 1. Create your capstone working folder

The payload is harmless JavaScript source. Keep it as data during analysis.

```bash
mkdir -p work/create
cat inputs/capstone_payload.js
```

**Expected:** A trainingEvent object and console print.



### 2. Apply rotation and XOR

Apply two routines you practiced. The sequence matters.

```bash
python3 labs/02_rot32.py encode inputs/capstone_payload.js work/create/rotated.txt
python3 labs/04_xor.py encode work/create/rotated.txt work/create/xor.bin --key 92
```

**Expected:** Rotated text, followed by XOR ciphertext bytes.



### 3. Compress and AES-encrypt

Compress the XOR bytes, then protect them using your own AES key.

```bash
python3 labs/03_gzip.py compress work/create/xor.bin work/create/payload.gz
node labs/05_aes.js keygen keys/student_capstone.key
node labs/05_aes.js encrypt work/create/payload.gz work/create/aes.json keys/student_capstone.key
```

**Expected:** A gzip file and an authenticated AES packet.



### 4. Wrap the AES key with RSA

Hybrid encryption: RSA protects the short AES key. AES protects the full data.

```bash
node labs/06_rsa.js keygen keys/student_capstone
node labs/06_rsa.js encrypt keys/student_capstone.key work/create/wrapped_key.b64 keys/student_capstone.public.pem
```

**Expected:** RSA ciphertext containing the encrypted AES key.



### 5. Package and Base64-encode one final file

package only combines existing fields. Base64 creates the final text artifact.

```bash
python3 exercises/capstone.py package --directory work/create --envelope work/create/envelope.json
python3 labs/01_base64.py encode work/create/envelope.json work/create/my_capstone.b64
```

**Expected:** One final file: work/create/my_capstone.b64.



## Capstone: recover the supplied all-layers file

The prebuilt artifact is `challenges/all_layers.b64`. Its matching teaching private key is `keys/capstone.private.pem`. Use that key for the supplied artifact. To recover your own artifact, replace the outer input with `work/create/my_capstone.b64` and use `keys/student_capstone.private.pem`; the remaining recovery sequence is identical.


### 1. Decode the supplied final file

Base64 is the outside representation of a packet carrying encrypted data and an RSA-wrapped AES key.

```bash
mkdir -p work/capstone
python3 labs/01_base64.py decode challenges/all_layers.b64 work/capstone/envelope.json
cat work/capstone/envelope.json
```

**Expected:** A JSON envelope with wrapped_key_b64 and aes_packet.



### 2. Extract the two encrypted fields

This helper separates fields into files. It performs no decryption.

```bash
python3 exercises/capstone.py extract
```

**Expected:** work/capstone/wrapped_key.b64 and work/capstone/aes.json.



### 3. Recover the AES key with RSA

Use the supplied matching private key. The output is a binary AES key.

```bash
node labs/06_rsa.js decrypt work/capstone/wrapped_key.b64 work/capstone/aes.key keys/capstone.private.pem
```

**Expected:** A 32-byte key. Check with: wc -c work/capstone/aes.key



### 4. Decrypt AES, then decompress gzip

Verify AES-GCM authentication before saving gzip bytes, then decompress.

```bash
node labs/05_aes.js decrypt work/capstone/aes.json work/capstone/payload.gz work/capstone/aes.key
python3 labs/03_gzip.py decompress work/capstone/payload.gz work/capstone/xor.bin
```

**Expected:** XOR ciphertext bytes remain after decompression.



### 5. Reverse XOR and the rotation

Reverse the inner transformations in the opposite order from construction.

```bash
python3 labs/04_xor.py decode work/capstone/xor.bin work/capstone/rotated.txt --key 92
python3 labs/02_rot32.py decode work/capstone/rotated.txt work/capstone/recovered.js
```

**Expected:** Readable harmless JavaScript source, without executing it.



### 6. Inspect and verify the payload

Compare exact bytes to the original. A URL string alone does not show a network action.

```bash
cat work/capstone/recovered.js
python3 exercises/capstone.py verify
```

**Expected:** PASS with a SHA-256 fingerprint.



## Ransomware connection and recovery case

Some ransomware uses hybrid encryption: a symmetric cipher protects data while an asymmetric key protects file keys. Implementations differ, and this exercise does not represent every family. Recognizing AES or RSA alone does not make decryption possible. Here the instructor supplies the correct private key.


This case generator creates three fixed synthetic documents in memory and writes encrypted training evidence. It never enumerates directories, takes user documents as input, removes originals, changes backups, or contacts a server. The event CSV and note are synthetic evidence. Real response requires scope assessment, coordinated containment, evidence preservation, and trusted recovery procedures.


### 1. Inspect and preserve the supplied case

All events are synthetic. Record source evidence before recovery.

```bash
cat challenges/incident/READ_ME_TRAINING.txt
cat challenges/incident/events.csv
sha256sum challenges/incident/bundle.lab.b64
```

**Expected:** Three synthetic encrypted-copy events and a training note.



### 2. Decode the evidence bundle

Decode Base64 and split the three records. No decryption happens in extract.

```bash
mkdir -p work/incident/recovered
python3 labs/01_base64.py decode challenges/incident/bundle.lab.b64 work/incident/bundle.json
python3 exercises/incident.py extract
```

**Expected:** Three AES packets and three RSA-wrapped keys under work/incident.



### 3. Recover the first document key

The incident private key is supplied by the instructor for this exercise.

```bash
node labs/06_rsa.js decrypt work/incident/invoice.txt.wrapped.b64 work/incident/invoice.key keys/incident.private.pem
```

**Expected:** A recovered 32-byte AES key for invoice.txt.



### 4. Restore the first document

Use the recovered file key to authenticate and decrypt the invoice packet.

```bash
node labs/05_aes.js decrypt work/incident/invoice.txt.aes.json work/incident/recovered/invoice.txt work/incident/invoice.key
cat work/incident/recovered/invoice.txt
```

**Expected:** TRAINING INVOICE, Example Company, 125.00 USD.



### 5. Restore the remaining documents

Apply the same recovery workflow to the remaining fixed training records.

```bash
for name in staff.csv recovery-plan.txt; do
  node labs/06_rsa.js decrypt "work/incident/$name.wrapped.b64" "work/incident/$name.key" keys/incident.private.pem
  node labs/05_aes.js decrypt "work/incident/$name.aes.json" "work/incident/recovered/$name" "work/incident/$name.key"
done
```

**Expected:** staff.csv and recovery-plan.txt appear in the recovered directory.



### 6. Validate and report recovery

The verifier compares each recovered document’s SHA-256 to a known-good baseline.

```bash
python3 exercises/incident.py verify
```

**Expected:** Three PASS lines, one for each document.



### Discussion

What indicators support encrypted-for-impact activity? Which facts come only from synthetic telemetry? What private key enabled recovery? What would be blocked without it? How would you preserve volatile evidence, contain affected systems, protect backups and verify restoration in a real incident?


## Primary references

- RFC 4648: https://www.rfc-editor.org/rfc/rfc4648.html
- RFC 1952: https://www.rfc-editor.org/rfc/rfc1952.html
- RFC 8017: https://www.rfc-editor.org/rfc/rfc8017.html
- Node crypto: https://nodejs.org/api/crypto.html
- MITRE ATT&CK T1486: https://attack.mitre.org/techniques/T1486/
- CISA ransomware guide: https://www.cisa.gov/stopransomware/ransomware-guide
