import sys
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from api_client import APIClientError, request_json


class CaesarWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        form_path = Path(__file__).resolve().parent / "ui" / "caesar.ui"
        uic.loadUi(str(form_path), self)
        self.btn_encrypt.clicked.connect(self.encrypt_text)
        self.btn_decrypt.clicked.connect(self.decrypt_text)

    def encrypt_text(self) -> None:
        try:
            key = int(self.txt_key.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid key", "Enter an integer key.")
            return

        try:
            result = request_json(
                "POST",
                "/api/caesar/encrypt",
                json={
                    "plain_text": self.txt_plain_text.toPlainText(),
                    "key": key,
                },
            )
        except APIClientError as exc:
            QMessageBox.critical(self, "Caesar API error", str(exc))
            return

        self.txt_cipher_text.setPlainText(str(result["encrypted_message"]))

    def decrypt_text(self) -> None:
        try:
            key = int(self.txt_key.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid key", "Enter an integer key.")
            return

        try:
            result = request_json(
                "POST",
                "/api/caesar/decrypt",
                json={
                    "cipher_text": self.txt_cipher_text.toPlainText(),
                    "key": key,
                },
            )
        except APIClientError as exc:
            QMessageBox.critical(self, "Caesar API error", str(exc))
            return

        self.txt_plain_text.setPlainText(str(result["decrypted_message"]))


def main() -> int:
    app = QApplication(sys.argv)
    window = CaesarWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
