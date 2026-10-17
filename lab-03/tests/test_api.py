import tempfile
import unittest
from pathlib import Path

import api
from cipher.rsa import RSACipher


class Lab03APITests(unittest.TestCase):
    def setUp(self) -> None:
        self.keys_directory = tempfile.TemporaryDirectory()
        self.original_cipher = api.rsa_cipher
        api.rsa_cipher = RSACipher(Path(self.keys_directory.name))
        api.app.config.update(TESTING=True)
        self.client = api.app.test_client()

    def tearDown(self) -> None:
        api.rsa_cipher = self.original_cipher
        self.keys_directory.cleanup()

    def test_rsa_encrypt_decrypt_sign_and_verify(self) -> None:
        generated = self.client.get("/api/rsa/generate_keys")
        self.assertEqual(generated.status_code, 200)

        encrypted = self.client.post(
            "/api/rsa/encrypt",
            json={"message": "HUTECH University", "key_type": "public"},
        )
        self.assertEqual(encrypted.status_code, 200)

        decrypted = self.client.post(
            "/api/rsa/decrypt",
            json={
                "ciphertext": encrypted.json["encrypted_message"],
                "key_type": "private",
            },
        )
        self.assertEqual(decrypted.status_code, 200)
        self.assertEqual(decrypted.json["decrypted_message"], "HUTECH University")

        signed = self.client.post(
            "/api/rsa/sign",
            json={"message": "HUTECH University"},
        )
        self.assertEqual(signed.status_code, 200)

        verified = self.client.post(
            "/api/rsa/verify",
            json={
                "message": "HUTECH University",
                "signature": signed.json["signature"],
            },
        )
        self.assertEqual(verified.status_code, 200)
        self.assertTrue(verified.json["is_verified"])

        tampered = self.client.post(
            "/api/rsa/verify",
            json={
                "message": "Different message",
                "signature": signed.json["signature"],
            },
        )
        self.assertEqual(tampered.status_code, 200)
        self.assertFalse(tampered.json["is_verified"])

    def test_rsa_requires_keys_before_encryption(self) -> None:
        response = self.client.post(
            "/api/rsa/encrypt",
            json={"message": "test", "key_type": "public"},
        )
        self.assertEqual(response.status_code, 409)
        self.assertIn("Generate", response.json["error"])

    def test_rsa_rejects_messages_over_pkcs1_v15_limit(self) -> None:
        self.client.get("/api/rsa/generate_keys")
        response = self.client.post(
            "/api/rsa/encrypt",
            json={"message": "A" * 246, "key_type": "public"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("245", response.json["error"])


if __name__ == "__main__":
    unittest.main()
