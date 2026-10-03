from flask import Flask, render_template, request
from cipher.caesar.caesar_cipher import CaesarCipher

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/caesar", methods=['GET'])
def caesar_web():
    return render_template('caesar.html')

@app.route("/caesar/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    caesar = CaesarCipher()
    encrypted_text = caesar.encrypt_text(text, key)
    return f'''
    <body style="font-family: Arial; padding: 30px;">
        <h2>KẾT QUẢ MÃ HÓA CAESAR</h2>
        <p><b>Plain text:</b> {text}</p>
        <p><b>Key:</b> {key}</p>
        <p style="color: blue;"><b>Encrypted text:</b> {encrypted_text}</p>
        <br><a href="/caesar">Quay lại</a>
    </body>
    '''

@app.route("/caesar/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    caesar = CaesarCipher()
    decrypted_text = caesar.decrypt_text(text, key)
    return f'''
    <body style="font-family: Arial; padding: 30px;">
        <h2>KẾT QUẢ GIẢI MÃ CAESAR</h2>
        <p><b>Cipher text:</b> {text}</p>
        <p><b>Key:</b> {key}</p>
        <p style="color: green;"><b>Decrypted text:</b> {decrypted_text}</p>
        <br><a href="/caesar">Quay lại</a>
    </body>
    '''

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)