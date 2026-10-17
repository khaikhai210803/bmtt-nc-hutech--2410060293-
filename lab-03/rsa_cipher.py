import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from api_client import APIClientError, request_json
from ui.rsa import Ui_RSAMainWindow


class RSAWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_RSAMainWindow()
        self.ui.setupUi(self)
        self.ui.btn_gen_keys.clicked.connect(self.generate_keys)
        self.ui.btn_encrypt.clicked.connect(self.encrypt_message)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_message)
        self.ui.btn_sign.clicked.connect(self.sign_message)
        self.ui.btn_verify.clicked.connect(self.verify_signature)

    def _request(self, method: str, path: str, **kwargs: object) -> dict[str, object] | None:
        try:
            return request_json(method, path, **kwargs)
        except APIClientError as exc:
            QMessageBox.critical(self, "RSA API error", str(exc))
            return None

    def generate_keys(self) -> None:
        result = self._request("GET", "/api/rsa/generate_keys")
        if result is not None:
            QMessageBox.information(self, "RSA", str(result["message"]))

    def encrypt_message(self) -> None:
        result = self._request(
            "POST",
            "/api/rsa/encrypt",
            json={
                "message": self.ui.txt_plain_text.toPlainText(),
                "key_type": "public",
            },
        )
        if result is not None:
            self.ui.txt_cipher_text.setPlainText(str(result["encrypted_message"]))

    def decrypt_message(self) -> None:
        result = self._request(
            "POST",
            "/api/rsa/decrypt",
            json={
                "ciphertext": self.ui.txt_cipher_text.toPlainText(),
                "key_type": "private",
            },
        )
        if result is not None:
            self.ui.txt_plain_text.setPlainText(str(result["decrypted_message"]))

    def sign_message(self) -> None:
        result = self._request(
            "POST",
            "/api/rsa/sign",
            json={"message": self.ui.txt_info.toPlainText()},
        )
        if result is not None:
            self.ui.txt_sign.setPlainText(str(result["signature"]))

    def verify_signature(self) -> None:
        result = self._request(
            "POST",
            "/api/rsa/verify",
            json={
                "message": self.ui.txt_info.toPlainText(),
                "signature": self.ui.txt_sign.toPlainText(),
            },
        )
        if result is None:
            return

        if result["is_verified"]:
            QMessageBox.information(self, "RSA", "Signature verified successfully.")
        else:
            QMessageBox.warning(self, "RSA", "Signature verification failed.")


def main() -> int:
    app = QApplication(sys.argv)
    window = RSAWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
