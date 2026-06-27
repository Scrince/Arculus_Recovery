import { test, expect } from './fixtures/yellowsphere-app.js';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  decryptArcV3Reference,
  decryptKeyfileV2Reference,
  fromBase64,
} from './helpers/crypto-reference.js';

const mnemonic12 = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about';
const mnemonic24 = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art';
const rawKeyfile = Uint8Array.from({ length: 64 }, (_, index) => (index * 17 + 11) & 0xff);
const keyfileSecret = `arc-keyfile-v1:${Buffer.from(rawKeyfile).toString('base64')}`;
const appHtmlPath = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'YellowSphere.html');

async function gotoPromotedApp(page) {
  await page.goto(new URL('YellowSphere.html', page.url()).toString());
  await expect(page).toHaveTitle('YellowSphere v1.6.6');
  await expect(page.locator('#status')).toHaveText('Ready');
}

async function encryptV3(page, mnemonic, credential, mode = '') {
  return page.evaluate(
    async ({ phrase, suppliedCredential, suppliedMode }) => encrypt_v3(phrase, suppliedCredential, suppliedMode),
    { phrase: mnemonic, suppliedCredential: credential, suppliedMode: mode },
  );
}

async function decryptV3(page, bundle, credential) {
  return page.evaluate(
    async ({ encryptedBundle, suppliedCredential }) => decryptV3(encryptedBundle, suppliedCredential),
    { encryptedBundle: bundle, suppliedCredential: credential },
  );
}

async function applicationRejects(page, functionName, args) {
  return page.evaluate(async ({ name, values }) => {
    try {
      await globalThis[name](...values);
      return false;
    } catch {
      return true;
    }
  }, { name: functionName, values: args });
}

function rawKeyfileText() {
  return JSON.stringify({
    magic: 'YELLOWSPHERE-KEYFILE',
    format: 'yellowsphere-keyfile-v1',
    version: 1,
    key_b64: Buffer.from(rawKeyfile).toString('base64'),
  }, null, 2);
}

async function dropFile(page, selector, { name, contents, mimeType = 'application/json' }) {
  await page.locator(selector).evaluate((target, file) => {
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(new File([file.contents], file.name, { type: file.mimeType }));
    for (const eventName of ['dragenter', 'dragover', 'drop']) {
      target.dispatchEvent(new DragEvent(eventName, {
        bubbles: true,
        cancelable: true,
        dataTransfer,
      }));
    }
  }, { name, contents, mimeType });
}

async function importSeedBundle(page, bundleText, filename = 'test-seed.arc') {
  await page.locator('#importSeedFile').setInputFiles({
    name: filename,
    mimeType: 'application/json',
    buffer: Buffer.from(bundleText),
  });
  await expect(page.locator('#arcCredentialDialog')).toHaveAttribute('open', '');
}

async function expectImportedSeed(page, sourceName) {
  await expect(page.locator('#arcCredentialDialog')).not.toHaveAttribute('open', '');
  await expect(page.locator('#status')).toContainText('Encrypted seed imported');
  const output = JSON.parse(await page.locator('#output').inputValue());
  expect(output).toMatchObject({
    imported_seed: 'loaded',
    source: sourceName,
    hidden_on_screen: true,
  });
}

test('ARC v3 matches independent Web Crypto for every credential mode', async ({ appPage: page }) => {
  const combinedCredential = {
    credentialMode: 'both',
    password: 'pässphrase',
    keyfileSecret,
  };
  const cases = [
    { mode: 'password', credential: 'correct horse battery staple', mnemonic: mnemonic12 },
    { mode: 'keyfile', credential: keyfileSecret, mnemonic: mnemonic24 },
    { mode: 'both', credential: combinedCredential, mnemonic: mnemonic12 },
  ];

  for (const testCase of cases) {
    const bundle = await encryptV3(page, testCase.mnemonic, testCase.credential);
    expect(bundle).toMatchObject({
      magic: 'YELLOWSPHERE-ARC',
      format: 'yellowsphere-encrypted-seed-v3',
      version: 3,
      credential_mode: testCase.mode,
      cipher: { name: 'AES-256-GCM' },
      padding: { name: 'ZERO', length: 512 },
    });
    expect(fromBase64(bundle.kdf.salt_b64)).toHaveLength(32);
    expect(fromBase64(bundle.cipher.nonce_b64)).toHaveLength(12);
    expect(fromBase64(bundle.ciphertext_b64)).toHaveLength(528);
    expect(bundle).not.toHaveProperty('mac_b64');
    expect(await decryptV3(page, bundle, testCase.credential)).toBe(testCase.mnemonic);

    const reference = await decryptArcV3Reference(bundle, testCase.credential);
    expect(reference.plaintext).toHaveLength(512);
    expect(reference.payload.mnemonic).toBe(testCase.mnemonic);
    expect(reference.payload.word_count).toBe(testCase.mode === 'keyfile' ? 24 : 12);
  }
});

test('ARC v3 rejects wrong credentials and authenticated-data tampering', async ({ appPage: page }) => {
  const credential = 'right password';
  const bundle = await encryptV3(page, mnemonic12, credential);

  expect(await applicationRejects(page, 'decryptV3', [bundle, 'wrong password'])).toBe(true);

  const headerTamper = structuredClone(bundle);
  headerTamper.created_at = '2000-01-01T00:00:00.000Z';
  expect(await applicationRejects(page, 'decryptV3', [headerTamper, credential])).toBe(true);

  const modeTamper = structuredClone(bundle);
  modeTamper.credential_mode = 'keyfile';
  expect(await applicationRejects(page, 'decryptV3', [modeTamper, credential])).toBe(true);

  const ciphertextTamper = structuredClone(bundle);
  const ciphertext = fromBase64(ciphertextTamper.ciphertext_b64);
  ciphertext[0] ^= 1;
  ciphertextTamper.ciphertext_b64 = Buffer.from(ciphertext).toString('base64');
  expect(await applicationRejects(page, 'decryptV3', [ciphertextTamper, credential])).toBe(true);
});

test('ARC v3 treats reserved-looking passwords as passwords when mode is explicit', async ({ appPage: page }) => {
  const password = 'arc-keyfile-v1:this-is-still-a-password';
  const bundle = await encryptV3(page, mnemonic12, password, 'password');

  expect(bundle.credential_mode).toBe('password');
  expect(bundle.kdf).toMatchObject({ name: 'PBKDF2', hash: 'SHA-512', iterations: 1000000 });
  expect(await decryptV3(page, bundle, password)).toBe(mnemonic12);
});

test('credential dialog clears password fields when closed', async ({ appPage: page }) => {
  await page.evaluate(() => { void requestArcCredential('import', 'password', true); });
  await page.locator('#arcPasswordInput').fill('temporary secret');
  await page.locator('#arcCredentialCancelBtn').click();

  await expect(page.locator('#arcCredentialDialog')).not.toHaveAttribute('open', '');
  await expect(page.locator('#arcPasswordInput')).toHaveValue('');
  await expect(page.locator('#arcPasswordConfirmInput')).toHaveValue('');
});

test('password meter penalizes exact repeated patterns and labels its score cautiously', async ({ appPage: page }) => {
  await page.evaluate(() => { void requestArcCredential('export', 'password'); });
  await page.locator('#arcPasswordInput').fill('abc'.repeat(30));

  await expect(page.locator('#arcPasswordStatus')).toContainText('not an entropy guarantee');
  const score = await page.locator('#arcPasswordStatus').textContent();
  expect(Number(score.match(/(\d+) bits/)?.[1])).toBeLessThan(50);
  await page.locator('#arcCredentialCancelBtn').click();
});

test('encrypted keyfile v2 matches independent Web Crypto and rejects tampering', async ({ appPage: page }) => {
  const password = 'keyfile password';
  const bundle = await page.evaluate(
    async ({ bytes, suppliedPassword }) => encryptArcKeyfileBytes_v2(new Uint8Array(bytes), suppliedPassword),
    { bytes: Array.from(rawKeyfile), suppliedPassword: password },
  );

  expect(bundle).toMatchObject({
    magic: 'YELLOWSPHERE-KEYFILE-ENC',
    format: 'yellowsphere-keyfile-enc-v1',
    version: 2,
    kdf: { algo: 'PBKDF2-SHA512', iterations: 1000000, prehash: 'SHA-512' },
    cipher: { name: 'AES-256-GCM' },
  });
  expect(fromBase64(bundle.kdf.salt_b64)).toHaveLength(16);
  expect(fromBase64(bundle.cipher.nonce_b64)).toHaveLength(12);
  expect(fromBase64(bundle.ciphertext_b64)).toHaveLength(80);
  expect(bundle).not.toHaveProperty('mac_b64');

  const applicationPlaintext = await page.evaluate(
    async ({ encryptedBundle, suppliedPassword }) => Array.from(
      await decryptArcKeyfileObject(encryptedBundle, suppliedPassword),
    ),
    { encryptedBundle: bundle, suppliedPassword: password },
  );
  expect(applicationPlaintext).toEqual(Array.from(rawKeyfile));
  expect(Buffer.from(await decryptKeyfileV2Reference(bundle, password))).toEqual(Buffer.from(rawKeyfile));
  expect(await applicationRejects(page, 'decryptArcKeyfileObject', [bundle, 'wrong password'])).toBe(true);

  const headerTamper = structuredClone(bundle);
  headerTamper.format += '-tampered';
  expect(await applicationRejects(page, 'decryptArcKeyfileObject_v2', [headerTamper, password])).toBe(true);

  const ciphertextTamper = structuredClone(bundle);
  const ciphertext = fromBase64(ciphertextTamper.ciphertext_b64);
  ciphertext[0] ^= 1;
  ciphertextTamper.ciphertext_b64 = Buffer.from(ciphertext).toString('base64');
  expect(await applicationRejects(page, 'decryptArcKeyfileObject', [ciphertextTamper, password])).toBe(true);
});

test('legacy ARC v2 and encrypted-keyfile v1 remain readable', async ({ appPage: page }) => {
  const legacyResults = await page.evaluate(async ({ phrase, secret, keyBytes }) => {
    const keyfileBytes = new Uint8Array(keyBytes);
    const combinedContainer = await combinedArcSecret('legacy combined password', secret);
    const cases = [
      { stored: 'legacy password', supplied: 'legacy password' },
      { stored: secret, supplied: secret },
      {
        stored: await combinedArcSecret_legacy('legacy combined password', secret),
        supplied: combinedContainer,
      },
    ];
    const arc = [];
    for (const testCase of cases) {
      const bundle = await encrypt_v2(phrase, testCase.stored);
      arc.push(await decrypt(bundle, testCase.supplied));
    }
    const oldKeyfile = await encryptArcKeyfileBytes(keyfileBytes, 'legacy keyfile password');
    const decryptedKeyfile = await decryptArcKeyfileObject(oldKeyfile, 'legacy keyfile password');
    return { arc, keyfile: Array.from(decryptedKeyfile) };
  }, { phrase: mnemonic12, secret: keyfileSecret, keyBytes: Array.from(rawKeyfile) });

  expect(legacyResults.arc).toEqual([mnemonic12, mnemonic12, mnemonic12]);
  expect(legacyResults.keyfile).toEqual(Array.from(rawKeyfile));
});

test('keyfile import supports the file picker', async ({ appPage: page }) => {
  await gotoPromotedApp(page);
  const bundleText = JSON.stringify(await encryptV3(page, mnemonic24, keyfileSecret, 'keyfile'));

  await importSeedBundle(page, bundleText, 'picker-keyfile.arc');
  await page.locator('#arcKeyfileInput').setInputFiles({
    name: 'YellowSphere_Keyfile.key',
    mimeType: 'application/json',
    buffer: Buffer.from(rawKeyfileText()),
  });
  await expect(page.locator('#arcKeyfileStatus')).toHaveText('Keyfile loaded.');
  await page.locator('#arcCredentialSubmitBtn').click();

  await expectImportedSeed(page, 'picker-keyfile.arc');
});

test('keyfile import supports drag and drop', async ({ appPage: page }) => {
  await gotoPromotedApp(page);
  const bundleText = JSON.stringify(await encryptV3(page, mnemonic24, keyfileSecret, 'keyfile'));

  await importSeedBundle(page, bundleText, 'dropped-keyfile.arc');
  await dropFile(page, '#arcKeyfileChooseRow', {
    name: 'Dropped_Keyfile.key',
    contents: rawKeyfileText(),
  });
  await expect(page.locator('#arcKeyfileChooseRow')).not.toHaveClass(/is-drag-over/);
  await expect(page.locator('#arcKeyfileStatus')).toHaveText('Keyfile loaded.');
  await page.locator('#arcCredentialSubmitBtn').click();

  await expectImportedSeed(page, 'dropped-keyfile.arc');
});

test('encrypted keyfile import unlocks combined-mode seed files', async ({ appPage: page }) => {
  await gotoPromotedApp(page);
  const password = 'combined keyfile password';
  const combinedCredential = { credentialMode: 'both', password, keyfileSecret };
  const bundleText = JSON.stringify(await encryptV3(page, mnemonic12, combinedCredential, 'both'));
  const encryptedKeyfileText = JSON.stringify(await page.evaluate(
    async ({ bytes, suppliedPassword }) => encryptArcKeyfileBytes_v2(new Uint8Array(bytes), suppliedPassword),
    { bytes: Array.from(rawKeyfile), suppliedPassword: password },
  ));

  await importSeedBundle(page, bundleText, 'encrypted-keyfile.arc');
  await page.locator('#arcPasswordInput').fill(password);
  await page.locator('#arcKeyfileInput').setInputFiles({
    name: 'YellowSphere_Keyfile.enc.key',
    mimeType: 'application/json',
    buffer: Buffer.from(encryptedKeyfileText),
  });
  await expect(page.locator('#arcKeyfileStatus')).toHaveText('Keyfile loaded.');
  await page.locator('#arcCredentialSubmitBtn').click();

  await expectImportedSeed(page, 'encrypted-keyfile.arc');
});

test('seed import reports wrong password without closing the dialog', async ({ appPage: page }) => {
  await gotoPromotedApp(page);
  const bundleText = JSON.stringify(await encryptV3(page, mnemonic12, 'correct password', 'password'));

  await importSeedBundle(page, bundleText, 'wrong-password.arc');
  await page.locator('#arcPasswordInput').fill('wrong password');
  await page.locator('#arcCredentialSubmitBtn').click();

  await expect(page.locator('#arcCredentialDialog')).not.toHaveAttribute('open', '');
  await expect(page.locator('#status')).toHaveText(
    'Error: Unable to decrypt seed file. The password may be incorrect or the file may be corrupted.',
  );
  await expect(page.locator('#output')).toHaveValue(/Unable to decrypt seed file/);
});

test('CSP allows every inline script by current hash only', async () => {
  const html = await readFile(appHtmlPath, 'utf8');
  const csp = html.match(/<meta http-equiv="Content-Security-Policy" content="([^"]+)"/)?.[1] || '';
  const scripts = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)].map((match) => match[1]);
  const hashes = scripts.map((script) => createHash('sha256').update(script, 'utf8').digest('base64'));

  expect(scripts).toHaveLength(2);
  expect(new Set(hashes).size).toBe(hashes.length);
  for (const hash of hashes) {
    expect(csp).toContain(`'sha256-${hash}'`);
  }
  expect([...csp.matchAll(/'sha256-([^']+)'/g)].map((match) => match[1]).sort()).toEqual([...hashes].sort());
});
