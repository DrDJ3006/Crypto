import hashlib
import hmac
import os
import sys
class Aes:
    def __init__(self, key_size):        
        if key_size == 128 :
            self.key_bytes_size = 16
            self.n_rounds = 10
        elif key_size == 192 :
            self.key_bytes_size = 24
            self.n_rounds = 12
        elif key_size == 256 :
            self.key_bytes_size = 32
            self.n_rounds = 14
        else:
            raise ValueError("Invalid key size: key size must be 128, 192, or 256 bits")
        self.s_box = (
            0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76, 0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15, 0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84, 0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8, 0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73, 0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, 0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A, 0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF, 0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
        )
        self.inv_s_box = (
            0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB, 0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
            0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E, 0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
            0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92, 0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
            0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06, 0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
            0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73, 0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
            0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B, 0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
            0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F, 0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
            0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
        )
        self.r_con = (
            0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
            0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
            0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
            0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
        )

    def expand_key(self,master_key):
        key_columns = self.bytes2matrix(master_key)
        iteration_size = len(master_key) // 4
        i = 1
        while len(key_columns) < (self.n_rounds + 1) * 4:
            word = list(key_columns[-1])
            if len(key_columns) % iteration_size == 0:
                word.append(word.pop(0))
                word = [self.s_box[b] for b in word]
                word[0] ^= self.r_con[i]
                i += 1
            elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
                word = [self.s_box[b] for b in word]
            word = bytes(i^j for i, j in zip(word, key_columns[-iteration_size]))
            key_columns.append(word)

        return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]

    
    def bytes2matrix(self, data: bytes):
        # Check if the data length is 16, 24, or 32 bytes
        if len(data) not in (16, 24, 32):
            raise ValueError("Data must be 16, 24, or 32 bytes long")
        
        # Determine the number of columns in the matrix
        columns = len(data) // 4
        
        # Convert bytes to matrix
        return [list(data[i:i+4]) for i in range(0, len(data), 4)]
    
    def matrix2bytes(self, matrix : tuple):
        byte_array = []
        for row in matrix:
            for element in row:
                byte_array.append(element)
        return bytes(byte_array)
    
    def sub_bytes(self, s):
        for i in range(len(s)):
            for j in range(len(s[i])):
                s[i][j] = self.s_box[s[i][j]]
        return s
    
    def inv_sub_bytes(self, s):
        for i in range(len(s)):
            for j in range(len(s[i])):
                s[i][j] = self.inv_s_box[s[i][j]]
        return s
    
    def add_round_key(self, s, k):
        for i in range(len(s)):
            for j in range(len(s[i])):
                s[i][j] = (s[i][j] ^ k[i][j])
        return s
    
    def mix_columns(self,s):
        for i in range(4):
            t = s[i][0] ^ s[i][1] ^ s[i][2] ^ s[i][3]
            u = s[i][0]
            s[i][0] ^= t ^ self.xtime(s[i][0] ^ s[i][1])
            s[i][1] ^= t ^ self.xtime(s[i][1] ^ s[i][2])
            s[i][2] ^= t ^ self.xtime(s[i][2] ^ s[i][3])
            s[i][3] ^= t ^ self.xtime(s[i][3] ^ u)
        return s

    def inv_mix_columns(self,s):
        for i in range(4):
            u = self.xtime(self.xtime(s[i][0] ^ s[i][2]))
            v = self.xtime(self.xtime(s[i][1] ^ s[i][3]))
            s[i][0] ^= u
            s[i][1] ^= v
            s[i][2] ^= u
            s[i][3] ^= v

        return self.mix_columns(s)  # Re-use mix_columns with adjusted coefficients
    
    def xtime(self,a):
        return ((a << 1) ^ 0x1B if a & 0x80 else a << 1) & 0xFF

    def shift_rows(self, s):
        s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
        s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]
        return s

    def inv_shift_rows(self,s):
        s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
        s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]
        return s
    
    def encrypt_block(self, key, plaintext):
        round_keys = self.expand_key(key)
        state = self.bytes2matrix(plaintext)
        self.add_round_key(state,round_keys[0])
        for i in range(1, self.n_rounds):
            self.sub_bytes(state)
            self.shift_rows(state)
            self.mix_columns(state)
            self.add_round_key(state,round_keys[i]) 
        self.sub_bytes(state)
        self.shift_rows(state)
        self.add_round_key(state,round_keys[self.n_rounds])
        ciphertext = self.matrix2bytes(state)
        return ciphertext

    def decrypt_block(self, key, ciphertext):
        round_keys = self.expand_key(key) # Remember to start from the last round key and work backwards through them when decrypting

        # Convert ciphertext to state matrix
        state = self.bytes2matrix(ciphertext)
        # Initial add round key step
        self.add_round_key(state,round_keys[self.n_rounds])
        for i in range(self.n_rounds - 1, 0, -1):
            self.inv_shift_rows(state)
            self.inv_sub_bytes(state)
            self.add_round_key(state,round_keys[i])
            self.inv_mix_columns(state)
        
        # Run final round (skips the InvMixColumns step)
        self.inv_shift_rows(state)
        self.inv_sub_bytes(state)
        self.add_round_key(state,round_keys[0])
        # Convert state matrix to plaintext
        plaintext = self.matrix2bytes(state)

        return plaintext
    
    def encrypt(self, key, plain_text, enc_mod="ecb", initial_vector=None):
        if len(key) != self.key_bytes_size:
            key = hkdf(key, self.key_bytes_size)
        data = add_pkcs7_padding(plain_text)
        if enc_mod == "ecb":
            return b''.join([self.encrypt_block(key, data[i:i+16]) for i in range(0, len(data), 16)])
        if enc_mod == "cbc":
            if initial_vector is None:
                initial_vector = os.urandom(16)
            cipher_text = b''
            vector = initial_vector
            for i in range(0, len(data), 16):
                data_entry = xor(data[i:i+16], vector)
                encrypted_block = self.encrypt_block(key, data_entry)
                cipher_text += encrypted_block
                vector = encrypted_block
                print_progress_bar(i + 1, len(data))
            return initial_vector+cipher_text
        
    def decrypt(self, key, cipher_text, enc_mod="ecb"):
        if len(key) != self.key_bytes_size:
            key = hkdf(key, self.key_bytes_size)
        
        if enc_mod == "ecb":
            return remove_pkcs7_padding(
                b''.join([self.decrypt_block(key, cipher_text[i:i+16]) for i in range(0, len(cipher_text), 16)])
            )
        
        if enc_mod == "cbc":
            initial_vector = cipher_text[:16]
            cipher_text = cipher_text[16:]
            plain_text = b''
            vector = initial_vector
            for i in range(0, len(cipher_text), 16):
                decrypted_block = self.decrypt_block(key, cipher_text[i:i+16])
                plain_text += xor(decrypted_block, vector)
                vector = cipher_text[i:i+16]
                print_progress_bar(i + 1, len(cipher_text))
            return remove_pkcs7_padding(plain_text)

    def encrypt_file(self, key, source_file, dest_file, enc_mod="cbc", initial_vector=None):
        if len(key) != self.key_bytes_size:
            key = hkdf(key, self.key_bytes_size)
        if enc_mod == "cbc":
            with open(source_file, mode="rb") as f:
                data = add_pkcs7_padding(f.read())
            if initial_vector is None:
                initial_vector = os.urandom(16)
            cipher_text = b''
            vector = initial_vector
            with open(dest_file, mode="wb") as df:
                df.write(initial_vector)  # Write the initial vector at the beginning
                for i in range(0, len(data), 16):
                    data_entry = xor(data[i:i+16], vector)
                    encrypted_block = self.encrypt_block(key, data_entry)
                    cipher_text += encrypted_block
                    vector = encrypted_block
                    # Write every 1 KB of encrypted data to the destination file
                    if len(cipher_text) >= 16384:
                        df.write(cipher_text)
                        cipher_text = b''
                    # Print progress bar
                    print_progress_bar(i + 16, len(data))
                # Write any remaining cipher text
                if cipher_text:
                    df.write(cipher_text)

    def decrypt_file(self, key, source_file, dest_file, enc_mod="cbc"):
        if len(key) != self.key_bytes_size:
            key = hkdf(key, self.key_bytes_size)
        
        with open(source_file, mode="rb") as f:
            if enc_mod == "cbc":
                initial_vector = f.read(16)  # Read the initial vector from the start of the file
                cipher_text = f.read()

        if enc_mod == "cbc":
            decrypted_data_accumulator = b''  # To accumulate decrypted data
            vector = initial_vector
            with open(dest_file, mode="wb") as df:
                for i in range(0, len(cipher_text), 16):
                    decrypted_block = self.decrypt_block(key, cipher_text[i:i+16])
                    decrypted_data = xor(decrypted_block, vector)
                    decrypted_data_accumulator += decrypted_data
                    vector = cipher_text[i:i+16]  # Update the IV to the current ciphertext block for the next block decryption
                    print_progress_bar(i + 16, len(cipher_text))

                    # Check if accumulated data has reached 2KB or if it's the final block
                    if len(decrypted_data_accumulator) >= 16384 or i + 16 >= len(cipher_text):
                        df.write(decrypted_data_accumulator)
                        decrypted_data_accumulator = b''  # Reset the accumulator

                # Final padding removal and writing if any residual data remains
                final_plaintext = remove_pkcs7_padding(decrypted_data_accumulator)
                df.write(final_plaintext)
                
def print_progress_bar(iteration, total, length=50):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '=' * filled_length +">"+ '-' * (length - filled_length - 1)
    print(f'\r[{bar}] {percent}% Complete',flush=True,end="")

hash_function = hashlib.sha256

def hmac_digest(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hash_function).digest()


def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    if len(salt) == 0:
        salt = bytes([0] * hash_function().digest_size)
    return hmac_digest(salt, ikm)


def hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    t = b""
    okm = b""
    i = 0
    while len(okm) < length:
        i += 1
        t = hmac_digest(prk, t + info + bytes([i]))
        okm += t
    return okm[:length]


def hkdf(ikm: bytes, length: int, salt: bytes = b'',  info: bytes = b'') -> bytes:
    prk = hkdf_extract(salt, ikm)
    return hkdf_expand(prk, info, length)


def add_pkcs7_padding(data, block_size=16):
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    padded_data = data + padding
    return padded_data

def remove_pkcs7_padding(data):
    # Vérifier s'il y a au moins 16 octets dans la donnée
    if len(data) < 16:
        return data  # Pas assez de données pour retirer le padding
    # Extrait le dernier bloc de 16 octets
    last_block = data[-16:]
    # Récupérer la valeur du padding_byte
    padding_byte = last_block[-1]
    # Vérifier que le padding_byte est dans la plage 1-16
    if padding_byte > 0 and padding_byte <= 16:
        # Vérifier que les octets de padding sont corrects
        for i in range(padding_byte):
            if last_block[-i-1] != padding_byte:
                return data  # Le padding est incorrect
        # Si le padding est correct, retirer le padding du dernier bloc
        last_block = last_block[:-padding_byte]
        # Remplacer le dernier bloc dans la donnée d'origine
        return data[:-16] + last_block
    return data  # Pas de padding détecté


def xor(plain_text,vector):
    return bytes([a ^ b for a, b in zip(list(plain_text), list(vector))])