# Instructor delivery and answers

Use the deck with the Student Workbook. A suggested three-hour schedule is setup/concepts 15 minutes, six labs 72 minutes, capstone 45 minutes, ransomware case 40 minutes, and debrief 8 minutes. Extend practice as needed.

For each lab: explain its purpose, show the input, ask students to run the forward command, inspect the result, ask them to run the reverse command, compare exact bytes, then ask the checkpoint question. Avoid running both directions for them before they try.

Base64: representation, no secret. ROT32: explicit ASCII Caesar +32 modulo 26, reverse -32. gzip: compression with no secret. XOR: same operation reverses, weak one-byte key, no authentication. AES-GCM: shared 32-byte key, fresh nonce, authenticated recovery; wrong keys/tampering must fail before writing output. RSA-OAEP: public encrypts, matching private decrypts with OAEP SHA-256; 190-byte limit for this configuration. RSA wraps a 32-byte AES key in the capstone.

The capstone is one envelope with Base64 outside, AES-encrypted gzip/XOR/ROT content, and an RSA-wrapped AES key. Do not imply RSA directly encrypts the whole payload. The script exercises/capstone.py only packages or extracts already-created fields. It does not solve the cryptography.

Let students build their own artifact first, then recover challenges/all_layers.b64. For a peer challenge, exchange the artifact and its matching disposable teaching private key. The private key is necessary for this exercise. Withhold the original source if desired after the construction pass.

The ransomware case contains fixed synthetic evidence for 3 documents. No actual incident occurs. Discuss real-world differences: actors usually withhold private keys, encryption families vary, and recovery may require trusted backups or a valid family-specific decryptor. A file extension, encoded string or crypto API alone does not establish maliciousness.

Expected incident recovery: invoice.txt contains a training invoice for Example Company, 125.00 USD; staff.csv contains Alex/SOC and Morgan/DFIR; recovery-plan.txt states to validate against known-good hashes. exercises/incident.py verify should report 3 PASS lines.

Debrief response: identify the evidence and scope, coordinate containment, preserve evidence including volatile sources, protect backups, recover through an approved trusted path, and validate restored data. Do not infer real executions from the synthetic event fixture. References: CISA StopRansomware Guide and MITRE T1486, linked in the workbook.

Assessment: 1 point per individual lab for correct round-trip comparison (6), 2 for correctly explaining the capstone order/key wrap, 2 for recovering and verifying the incident documents. Suggested pass: 8/10 with an accurate key-requirement explanation.

Instructor validation: python3 instructor/verify_course.py. It uses a temporary copy, tests the exercise commands including expected failures, and removes its temporary copy automatically. It does not change student results.
