# SOC hands-on training kit

Start with Student_Workbook.md and SOC_Hands_On_Training.pptx.

Six individual practice labs each expose separate forward/reverse commands. Students transform their own supplied input, reverse their result, and compare exact bytes. The capstone combines all six routines into one harmless file. A final synthetic ransomware case applies AES/RSA recovery to three supplied document records.

Requirements: Ubuntu terminal, Python 3, and Node.js already installed. No third-party packages. Run from the root of this extracted folder. Do not run recovered JavaScript.

Folders: inputs/ contains practice text and harmless source; labs/ contains one file per routine plus shared Node crypto helpers; challenges/ contains ready-made cases; keys/ contains teaching keys for those cases; work/ holds student results; instructor/ contains answers and validation.

Every private key in this kit is a disposable teaching key. Never reuse it for real secrets. Practice key generation refuses to overwrite an existing key, so repeated exercises should reuse existing keys or use a new prefix.

Use the key that matches your artifact: supplied all_layers.b64 uses keys/capstone.private.pem; your created capstone uses keys/student_capstone.private.pem; incident evidence uses keys/incident.private.pem. The original capstone AES key is omitted from the distributed kit so students practice RSA recovery.
