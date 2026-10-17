from flask import Flask, jsonify, request

from cipher.caesar.caesar_cipher import CaesarCipher

app = Flask(__name__)
caesar_cipher = CaesarCipher()


def _error(message: str, status: int = 400):
    return jsonify({"error": message}), status


def _json_object() -> dict[str, object] | None:
    payload = request.get_json(silent=True)
    return payload if isinstance(payload, dict) else None


@app.post("/api/caesar/encrypt")
def encrypt():
    payload = _json_object()
    if payload is None:
        return _error("A JSON object is required.")

    plain_text = payload.get("plain_text")
    key = payload.get("key")
    if not isinstance(plain_text, str):
        return _error("'plain_text' must be a string.")
    if isinstance(key, bool) or not isinstance(key, int):
        return _error("'key' must be an integer.")

    encrypted_message = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({"encrypted_message": encrypted_message})


@app.post("/api/caesar/decrypt")
def decrypt():
    payload = _json_object()
    if payload is None:
        return _error("A JSON object is required.")

    cipher_text = payload.get("cipher_text")
    key = payload.get("key")
    if not isinstance(cipher_text, str):
        return _error("'cipher_text' must be a string.")
    if isinstance(key, bool) or not isinstance(key, int):
        return _error("'key' must be an integer.")

    decrypted_message = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({"decrypted_message": decrypted_message})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
