class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I").upper()
        matrix = list(key)
        for letter in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
            if letter not in set(key):
                matrix.append(letter)
        return [matrix[i:i+5] for i in range(0, 25, 5)]

    def find_position(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return None

    def encrypt_text(self, text, matrix):
        text = text.replace("J", "I").upper()
        text_len = len(text)
        if text_len % 2 != 0:
            text += "X"
        
        cipher_text = ""
        for i in range(0, len(text), 2):
            pair = text[i:i+2]
            r1, c1 = self.find_position(matrix, pair[0])
            r2, c2 = self.find_position(matrix, pair[1])
            
            if r1 == r2:
                cipher_text += matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
            elif c1 == c2:
                cipher_text += matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
            else:
                cipher_text += matrix[r1][c2] + matrix[r2][c1]
        return cipher_text

    def decrypt_text(self, text, matrix):
        text = text.upper()
        decrypted_text = ""
        for i in range(0, len(text), 2):
            pair = text[i:i+2]
            r1, c1 = self.find_position(matrix, pair[0])
            r2, c2 = self.find_position(matrix, pair[1])
            
            if r1 == r2:
                decrypted_text += matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
            elif c1 == c2:
                decrypted_text += matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
            else:
                decrypted_text += matrix[r1][c2] + matrix[r2][c1]
        return decrypted_text