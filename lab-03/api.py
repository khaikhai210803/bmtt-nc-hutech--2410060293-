from __future__ import annotations

from flask import Flask, jsonify, request
import rsa

from cipher.rsa import RSACipher

app = Flask(__name__)
rsa_cipher = RSACipher()


def _error(message: str, status: int = 400):
    return jsonify({"error": message}), status


def _payload() -> dict[str, object] | None:
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else None


def _string_field(data: dict[str, object], name: str) -> str | None:
    value = data.get(name)
    return value if isinstance(value, str) else None


def _keys_or_error():
    try:
        return rsa_cipher.load_keys(), None
    except FileNotFoundError:
        return None, _error("Generate RSA keys first.", 409)


@app.post("/api/caesar/encrypt")
def caesar_encrypt():
    data = _payload()
    if data is None:
        return _error("A JSON object is required.")

    plain_text = _string_field(data, "plain_text")
    key = data.get("key")
    if plain_text is None:
        return _error("'plain_text' must be a string.")
    if isinstance(key, bool) or not isinstance(key, int):
        return _error("'key' must be an integer.")

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    encrypted = "".join(
        alphabet[(alphabet.index(char) + key) % len(alphabet)]
        if char in alphabet
        else char
        for char in plain_text.upper()
    )
    return jsonify({"encrypted_message": encrypted})


@app.post("/api/caesar/decrypt")
def caesar_decrypt():
    data = _payload()
    if data is None:
        return _error("A JSON object is required.")

    cipher_text = _string_field(data, "cipher_text")
    key = data.get("key")
    if cipher_text is None:
        return _error("'cipher_text' must be a string.")
    if isinstance(key, bool) or not isinstance(key, int):
        return _error("'key' must be an integer.")

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    decrypted = "".join(
        alphabet[(alphabet.index(char) - key) % len(alphabet)]
        if char in alphabet
        else char
        for char in cipher_text.upper()
    )
    return jsonify({"decrypted_message": decrypted})


@app.get("/api/rsa/generate_keys")
def rsa_generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({"message": "RSA keys generated successfully."})


@app.post("/api/rsa/encrypt")
def rsa_encrypt():
    data = _payload()
    if data is None:
        return _error("A JSON object is required.")

    message = _string_field(data, "message")
    if message is None:
        return _error("'message' must be a string.")
    if data.get("key_type") != "public":
        return _error("RSA encryption requires key_type 'public'.")

    keys, error = _keys_or_error()
    if error is not None:
        return error
    _, public_key = keys

    max_length = (public_key.n.bit_length() + 7) // 8 - 11
    if len(message.encode("utf-8")) > max_length:
        return _error(
            f"Message is too long for this RSA key (maximum {max_length} UTF-8 bytes)."
        )
    try:
        ciphertext = rsa_cipher.encrypt(message, public_key)
    except (OverflowError, ValueError) as exc:
        return _error(str(exc))
    return jsonify({"encrypted_message": ciphertext.hex()})


@app.post("/api/rsa/decrypt")
def rsa_decrypt():
    data = _payload()
    if data is None:
        return _error("A JSON object is required.")

    ciphertext_hex = _string_field(data, "ciphertext")
    if ciphertext_hex is None:
        return _error("'ciphertext' must be a hexadecimal string.")
    if data.get("key_type") != "private":
        return _error("RSA decryption requires key_type 'private'.")

    keys, error = _keys_or_error()
    if error is not None:
        return error
    private_key, _ = keys
    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
        message = rsa_cipher.decrypt(ciphertext, private_key)
    except (ValueError, rsa.DecryptionError, UnicodeDecodeError) as exc:
        return _error(f"Cannot decrypt ciphertext: {exc}")
    return jsonify({"decrypted_message": message})


@app.post("/api/rsa/sign")
def rsa_sign():
    data = _payload()
    if data is None:
        return _error("A JSON object is required.")

    message = _string_field(data, "message")
    if message is None:
        return _error("'message' must be a string.")

    keys, error = _keys_or_error()
    if error is not None:
        return error
    private_key, _ = keys
    signature = rsa_cipher.sign(message, private_key)
    return jsonify({"signature": signature.hex()})


@app.post("/api/rsa/verify")
def rsa_verify():
    data = _payload()
    if data is None:
        return _error("A JSON object is required.")

    message = _string_field(data, "message")
    signature_hex = _string_field(data, "signature")
    if message is None:
        return _error("'message' must be a string.")
    if signature_hex is None:
        return _error("'signature' must be a hexadecimal string.")

    keys, error = _keys_or_error()
    if error is not None:
        return error
    _, public_key = keys
    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        return _error("'signature' must be a hexadecimal string.")

    is_verified = rsa_cipher.verify(message, signature, public_key)
    return jsonify({"is_verified": is_verified})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
