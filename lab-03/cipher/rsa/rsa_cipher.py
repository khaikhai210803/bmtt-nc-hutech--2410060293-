from pathlib import Path

import rsa


class RSACipher:
    def __init__(self, keys_directory: Path | None = None) -> None:
        self.keys_directory = (
            keys_directory
            if keys_directory is not None
            else Path(__file__).resolve().parent / "keys"
        )
        self.private_key_path = self.keys_directory / "privateKey.pem"
        self.public_key_path = self.keys_directory / "publicKey.pem"

    def generate_keys(
        self, key_size: int = 2048
    ) -> tuple[rsa.PublicKey, rsa.PrivateKey]:
        self.keys_directory.mkdir(parents=True, exist_ok=True)
        public_key, private_key = rsa.newkeys(key_size)
        self.private_key_path.write_bytes(private_key.save_pkcs1())
        self.public_key_path.write_bytes(public_key.save_pkcs1())
        return public_key, private_key

    def load_keys(self) -> tuple[rsa.PrivateKey, rsa.PublicKey]:
        if not self.private_key_path.is_file() or not self.public_key_path.is_file():
            raise FileNotFoundError(
                "RSA keys do not exist. Generate a key pair before using RSA."
            )

        private_key = rsa.PrivateKey.load_pkcs1(self.private_key_path.read_bytes())
        public_key = rsa.PublicKey.load_pkcs1(self.public_key_path.read_bytes())
        return private_key, public_key

    @staticmethod
    def encrypt(message: str, public_key: rsa.PublicKey) -> bytes:
        return rsa.encrypt(message.encode("utf-8"), public_key)

    @staticmethod
    def decrypt(ciphertext: bytes, private_key: rsa.PrivateKey) -> str:
        return rsa.decrypt(ciphertext, private_key).decode("utf-8")

    @staticmethod
    def sign(message: str, private_key: rsa.PrivateKey) -> bytes:
        return rsa.sign(message.encode("utf-8"), private_key, "SHA-256")

    @staticmethod
    def verify(
        message: str, signature: bytes, public_key: rsa.PublicKey
    ) -> bool:
        try:
            rsa.verify(message.encode("utf-8"), signature, public_key)
        except rsa.VerificationError:
            return False
        return True
