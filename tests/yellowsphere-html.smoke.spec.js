import { test, expect } from './fixtures/yellowsphere-app.js';

test('standalone production HTML critical browser flows', async ({ appPage: page }) => {

  await page.locator('#count').fill('1');
  await page.getByRole('button', { name: 'Generate Random Seed' }).click();
  await expect(page.locator('#status')).toContainText('Generated random 12-word mnemonic');
  await expect(page.locator('#rootFingerprintDisplay')).toHaveValue(/Root Fingerprint: [0-9a-f]{8}/i);

  await page.getByRole('button', { name: 'Validate Mnemonic' }).click();
  await expect(page.locator('#status')).toHaveText('Mnemonic is valid BIP39 (English word list + checksum).');
  const validation = JSON.parse(await page.locator('#output').inputValue());
  expect(validation.validation).toBe('ok');
  expect(validation.word_count).toBe(12);

  const coinOptions = await page.locator('#coin option').evaluateAll((options) =>
    options.map((option) => option.value),
  );

  for (const coin of coinOptions) {
    await page.locator('#coin').selectOption(coin);
    await page.locator('#count').fill('1');
    await page.getByRole('button', { name: 'Derive Keys + Addresses' }).click();
    await expect(page.locator('#status')).toHaveText(
      'Derivation complete. Seed phrase hidden — hold “Show Seed” to reveal.',
      { timeout: 15_000 },
    );

    const output = await page.locator('#output').inputValue();
    const parsed = JSON.parse(output);
    expect(parsed.accounts?.length, `${coin} should return one account`).toBe(1);
    expect(output, `${coin} should include at least one address field`).toContain('"address"');
  }

  await expect(page.getByRole('button', { name: 'Table View' })).toBeVisible();
  await page.getByRole('button', { name: 'Raw JSON' }).click();
  await page.getByRole('button', { name: 'Extended Keys' }).click();
  await expect(page.locator('#accountKeysPane')).toBeVisible();

  await page.getByRole('button', { name: 'Open settings' }).click();
  await expect(page.locator('#settingsDialog')).toHaveAttribute('open', '');
  await expect(page.locator('input[name="themeMode"]')).toHaveCount(4);
  await page.keyboard.press('Escape');
  await expect(page.locator('#settingsDialog')).not.toHaveAttribute('open', '');

  await page.getByRole('button', { name: 'QR Export' }).click();
  await expect(page.locator('#qrModal')).toHaveAttribute('open', '');
  await page.locator('#qrAddressInput').fill('bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kygt080');
  await page.getByRole('button', { name: 'Generate', exact: true }).click();
  await expect(page.locator('#qrCanvas')).toBeVisible();
  await expect(page.locator('#qrAddressLabel')).toContainText('bitcoin:');
  await page.keyboard.press('Escape');
  await expect(page.locator('#qrModal')).not.toHaveAttribute('open', '');

  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Export', exact: true }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toMatch(/^YellowSphere_Key_Export_.*\.pdf$/);
  await expect(page.locator('#status')).toHaveText('Key export saved as PDF.');
});

test('Cardano derivation applies the BIP39 passphrase', async ({ appPage: page }) => {
  const mnemonic = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about';
  await page.locator('#mnemonic').fill(mnemonic);
  await page.locator('#coin').selectOption('Cardano');
  await page.locator('#count').fill('1');

  await page.locator('#passphrase').fill('');
  await page.getByRole('button', { name: 'Derive Keys + Addresses' }).click();
  await expect(page.locator('#status')).toContainText('Derivation complete.', { timeout: 15_000 });
  const withoutPassphrase = JSON.parse(await page.locator('#output').inputValue());

  await page.locator('#passphrase').fill('TREZOR');
  await page.getByRole('button', { name: 'Derive Keys + Addresses' }).click();
  await expect(page.locator('#status')).toContainText('Derivation complete.', { timeout: 15_000 });
  const withPassphrase = JSON.parse(await page.locator('#output').inputValue());

  expect(withPassphrase.accounts[0].root_private_key_hex)
    .not.toBe(withoutPassphrase.accounts[0].root_private_key_hex);
  expect(withPassphrase.accounts[0].receiving[0].address)
    .not.toBe(withoutPassphrase.accounts[0].receiving[0].address);
});
