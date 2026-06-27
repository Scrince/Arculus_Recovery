from __future__ import annotations

import base64
import json
import unittest

from yellowsphere.core import (
    ARC_V2_NONCE_BYTES,
    ARC_V2_SALT_BYTES,
    analyze_mnemonic,
    bip39_to_seed,
    bip39_validate,
    cardano_icarus_master_from_entropy,
    decrypt_seed_bundle,
    encrypt_seed_bundle,
    format_derived_output,
    generate_random_mnemonic,
    mnemonic_entropy_bytes,
    parse_seed_bundle,
    run_derivation,
    serialize_seed_bundle,
)


MNEMONIC = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
BIP39_SEED_HEX = (
    "5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19"
    "a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4"
)
BIP84_ADDRESS = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"


class Bip39Tests(unittest.TestCase):
    def test_known_bip39_seed_vector(self) -> None:
        words_ok, checksum_ok, message = bip39_validate(MNEMONIC)
        self.assertTrue(words_ok, message)
        self.assertTrue(checksum_ok, message)
        self.assertEqual(bip39_to_seed(MNEMONIC, "").hex(), BIP39_SEED_HEX)

    def test_analysis_and_generation_for_supported_word_counts(self) -> None:
        analysis = analyze_mnemonic(MNEMONIC)
        self.assertEqual(analysis["word_count"], 12)
        self.assertTrue(analysis["checksum_ok"])
        for word_count in (12, 24):
            generated = generate_random_mnemonic(word_count)
            words_ok, checksum_ok, message = bip39_validate(generated)
            self.assertTrue(words_ok, message)
            self.assertTrue(checksum_ok, message)
            self.assertEqual(len(generated.split()), word_count)


class DerivationTests(unittest.TestCase):
    def test_known_bitcoin_bip84_address(self) -> None:
        output = run_derivation(
            mnemonic=MNEMONIC,
            passphrase="",
            derivation="m/84h/0h/0h",
            all_common=False,
            script_type="p2wpkh",
            count=1,
            coin="bitcoin",
            testnet=False,
        )
        account = output["accounts"][0]
        self.assertEqual(account["derivation"], "m/84'/0'/0'")
        self.assertEqual(account["receiving"][0]["address"], BIP84_ADDRESS)
        self.assertEqual(account["receiving"][0]["path"], "m/84'/0'/0'/0/0")

        json_output = json.loads(format_derived_output(output, "json"))
        self.assertEqual(json_output["coin"], "bitcoin")
        self.assertIn(BIP84_ADDRESS, format_derived_output(output, "csv"))
        self.assertIn(BIP84_ADDRESS, format_derived_output(output, "txt"))

    def test_invalid_count_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "count must be >= 1"):
            run_derivation(MNEMONIC, "", "", False, "auto", 0, "bitcoin", False)

    def test_cardano_bip39_passphrase_changes_derived_wallet(self) -> None:
        without_passphrase = run_derivation(MNEMONIC, "", "", False, "auto", 1, "cardano", False)
        with_passphrase = run_derivation(MNEMONIC, "TREZOR", "", False, "auto", 1, "cardano", False)

        empty_account = without_passphrase["accounts"][0]
        protected_account = with_passphrase["accounts"][0]
        self.assertNotEqual(empty_account["root_private_key_hex"], protected_account["root_private_key_hex"])
        self.assertNotEqual(
            empty_account["receiving"][0]["address"],
            protected_account["receiving"][0]["address"],
        )

    def test_cardano_icarus_passphrase_vector(self) -> None:
        mnemonic = "eight country switch draw meat scout mystery blade tip drift useless good keep usage title"
        expected = (
            "70531039904019351e1afb361cd1b312a4d0565d4ff9f8062d38acf4b15cce41"
            "d7b5738d9c893feea55512a3004acb0d222c35d3e3d5cde943a15a9824cbac59"
            "443cf67e589614076ba01e354b1a432e0e6db3b59e37fc56b5fb0222970a010e"
        )
        root = cardano_icarus_master_from_entropy(mnemonic_entropy_bytes(mnemonic), "foo")
        self.assertEqual((root["k"] + root["c"]).hex(), expected)


class ArcCompatibilityTests(unittest.TestCase):
    def test_arc_v2_round_trip_armor_and_field_sizes(self) -> None:
        bundle = encrypt_seed_bundle(MNEMONIC, "test password")
        self.assertEqual(bundle["version"], 2)
        self.assertEqual(len(base64.b64decode(bundle["kdf"]["salt_b64"])), ARC_V2_SALT_BYTES)
        self.assertEqual(len(base64.b64decode(bundle["cipher"]["nonce_b64"])), ARC_V2_NONCE_BYTES)
        self.assertEqual(len(base64.b64decode(bundle["mac_b64"])), 64)
        self.assertEqual(decrypt_seed_bundle(bundle, "test password"), MNEMONIC)

        armored = serialize_seed_bundle(bundle)
        reparsed = parse_seed_bundle(armored)
        self.assertEqual(reparsed, bundle)
        self.assertEqual(decrypt_seed_bundle(reparsed, "test password"), MNEMONIC)

    def test_arc_v2_rejects_wrong_password_and_tampering(self) -> None:
        bundle = encrypt_seed_bundle(MNEMONIC, "right password")
        with self.assertRaisesRegex(ValueError, "password may be incorrect"):
            decrypt_seed_bundle(bundle, "wrong password")

        tampered = json.loads(json.dumps(bundle))
        ciphertext = bytearray(base64.b64decode(tampered["ciphertext_b64"]))
        ciphertext[0] ^= 1
        tampered["ciphertext_b64"] = base64.b64encode(ciphertext).decode("ascii")
        with self.assertRaisesRegex(ValueError, "password may be incorrect"):
            decrypt_seed_bundle(tampered, "right password")


if __name__ == "__main__":
    unittest.main()
