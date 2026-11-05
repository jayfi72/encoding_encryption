// Harmless source text for the SOC capstone. Recovery never executes this file.
const trainingEvent = {
  exercise: 'All six routines recovered',
  urlAsData: 'https://training.invalid/checkin',
  message: 'Base64, ROT32, gzip, XOR-92, AES-GCM, and RSA-OAEP.'
};
console.log(JSON.stringify(trainingEvent, null, 2));
