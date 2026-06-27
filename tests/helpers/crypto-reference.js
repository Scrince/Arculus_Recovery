import { webcrypto } from 'node:crypto';

const { subtle } = webcrypto;
const encoder = new TextEncoder();
const decoder = new TextDecoder('utf-8', { fatal: true });

export const fromBase64 = (value) => new Uint8Array(Buffer.from(value, 'base64'));

async function pbkdf2AesKey(password, salt, iterations) {
  const passwordBytes = encoder.encode(password.normalize('NFKD'));
  const passwordHash = await subtle.digest('SHA-512', passwordBytes);
  const material = await subtle.importKey('raw', passwordHash, 'PBKDF2', false, ['deriveKey']);
  return subtle.deriveKey(
    { name: 'PBKDF2', hash: 'SHA-512', salt, iterations },
    material,
    { name: 'AES-GCM', length: 256 },
    false,
    ['decrypt'],
  );
}

async function hkdfAesKey(credential, salt) {
  const material = await subtle.importKey('raw', encoder.encode(credential), 'HKDF', false, ['deriveKey']);
  return subtle.deriveKey(
    {
      name: 'HKDF',
      hash: 'SHA-512',
      salt,
      info: encoder.encode('YellowSphere ARC v3 AES-256-GCM key'),
    },
    material,
    { name: 'AES-GCM', length: 256 },
    false,
    ['decrypt'],
  );
}

async function combinedCredential(password, keyfileSecret, salt) {
  const keyfileBytes = fromBase64(keyfileSecret.slice('arc-keyfile-v1:'.length));
  const passwordBytes = encoder.encode(password.normalize('NFKD'));
  const input = new Uint8Array(keyfileBytes.length + passwordBytes.length);
  input.set(keyfileBytes);
  input.set(passwordBytes, keyfileBytes.length);
  const material = await subtle.importKey('raw', input, 'HKDF', false, ['deriveBits']);
  const bits = await subtle.deriveBits(
    {
      name: 'HKDF',
      hash: 'SHA-512',
      salt,
      info: encoder.encode('yellowsphere-arc-v3-combined-key'),
    },
    material,
    512,
  );
  return `arc-combined-v1:${Buffer.from(bits).toString('base64')}`;
}

export async function decryptArcV3Reference(bundle, suppliedCredential) {
  const salt = fromBase64(bundle.kdf.salt_b64);
  const nonce = fromBase64(bundle.cipher.nonce_b64);
  const credential = suppliedCredential?.credentialMode === 'both'
    ? await combinedCredential(
      suppliedCredential.password,
      suppliedCredential.keyfileSecret,
      salt,
    )
    : suppliedCredential;
  const key = credential.startsWith('arc-keyfile-v1:') || credential.startsWith('arc-combined-v1:')
    ? await hkdfAesKey(credential, salt)
    : await pbkdf2AesKey(credential, salt, 1_000_000);
  const metadata = {};
  for (const name of Object.keys(bundle)) {
    if (name !== 'ciphertext_b64') metadata[name] = bundle[name];
  }
  const plaintext = new Uint8Array(await subtle.decrypt(
    {
      name: 'AES-GCM',
      iv: nonce,
      additionalData: encoder.encode(JSON.stringify(metadata)),
      tagLength: 128,
    },
    key,
    fromBase64(bundle.ciphertext_b64),
  ));
  let end = plaintext.length;
  while (end > 0 && plaintext[end - 1] === 0) end -= 1;
  return { plaintext, payload: JSON.parse(decoder.decode(plaintext.slice(0, end))) };
}

export async function decryptKeyfileV2Reference(bundle, password) {
  const salt = fromBase64(bundle.kdf.salt_b64);
  const key = await pbkdf2AesKey(password, salt, bundle.kdf.iterations);
  return new Uint8Array(await subtle.decrypt(
    {
      name: 'AES-GCM',
      iv: fromBase64(bundle.cipher.nonce_b64),
      additionalData: encoder.encode(JSON.stringify({ magic: bundle.magic, format: bundle.format })),
      tagLength: 128,
    },
    key,
    fromBase64(bundle.ciphertext_b64),
  ));
}
