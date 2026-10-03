from string import ascii_uppercase

class CaesarCipher:
    def __init__(self):
        self.alphabet = list(ascii_uppercase)

    def encrypt_text(self, text: str, key: int) -> str:
        text = text.upper()
        encrypted_text = []
        for letter in text:
            if letter in self.alphabet:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index + key) % len(self.alphabet)
                encrypted_text.append(self.alphabet[output_index])
            else:
                encrypted_text.append(letter)
        return "".join(encrypted_text)

    def decrypt_text(self, text: str, key: int) -> str:
        text = text.upper()
        decrypted_text = []
        for letter in text:
            if letter in self.alphabet:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index - key) % len(self.alphabet)
                decrypted_text.append(self.alphabet[output_index])
            else:
                decrypted_text.append(letter)
        return "".join(decrypted_text)