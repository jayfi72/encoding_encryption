#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p work/build
# Run each skill forward separately, then package the resulting ciphertext.
python3 labs/02_rot32.py encode inputs/capstone_payload.js work/build/rotated.txt
python3 labs/04_xor.py encode work/build/rotated.txt work/build/xor.bin --key 92
python3 labs/03_gzip.py compress work/build/xor.bin work/build/payload.gz
if [ ! -f keys/capstone_aes.key ]; then node labs/05_aes.js keygen keys/capstone_aes.key; fi
node labs/05_aes.js encrypt work/build/payload.gz work/build/aes.json keys/capstone_aes.key
if [ ! -f keys/capstone.public.pem ]; then node labs/06_rsa.js keygen keys/capstone; fi
node labs/06_rsa.js encrypt keys/capstone_aes.key work/build/wrapped_key.b64 keys/capstone.public.pem
python3 exercises/capstone.py package --directory work/build --envelope work/build/envelope.json
python3 labs/01_base64.py encode work/build/envelope.json work/build/all_layers.b64
cp work/build/all_layers.b64 challenges/all_layers.b64
if [ ! -f keys/incident.public.pem ]; then node labs/06_rsa.js keygen keys/incident; fi
node exercises/ransomware_case.js create
