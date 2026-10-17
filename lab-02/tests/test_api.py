import unittest

import api


class CaesarAPITests(unittest.TestCase):
    def setUp(self) -> None:
        api.app.config.update(TESTING=True)
        self.client = api.app.test_client()

    def test_encrypt_and_decrypt(self) -> None:
        encrypted = self.client.post(
            "/api/caesar/encrypt",
            json={"plain_text": "Attack at dawn!", "key": 3},
        )
        self.assertEqual(encrypted.status_code, 200)
        self.assertEqual(encrypted.json["encrypted_message"], "DWWDFN DW GDZQ!")

        decrypted = self.client.post(
            "/api/caesar/decrypt",
            json={"cipher_text": encrypted.json["encrypted_message"], "key": 3},
        )
        self.assertEqual(decrypted.status_code, 200)
        self.assertEqual(decrypted.json["decrypted_message"], "ATTACK AT DAWN!")

    def test_rejects_invalid_key(self) -> None:
        response = self.client.post(
            "/api/caesar/encrypt",
            json={"plain_text": "HELLO", "key": "3"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("integer", response.json["error"])


if __name__ == "__main__":
    unittest.main()
