# AES Encryption Algorithm Implementation in Python

This Python codebase implements the Advanced Encryption Standard (AES) encryption algorithm. It supports key sizes of 128, 192, and 256 bits. The primary purpose of this implementation is to facilitate educational and testing activities, allowing users to explore and understand the core concepts of AES encryption.

## Important Notice
**This implementation is intended for educational and testing purposes only.** Please refrain from using this code in real-world projects or production environments.

Before using this code, I recommend you study AES. In the bottom of this readme, you can find an explaination about AES.


## Features

- **Key Support:** AES-128, AES-192, AES-256.
- **Modes:** ECB, CBC.
- **Data Encryption/Decryption:** Encrypt and decrypt data with both ECB and CBC modes.
- **File Encryption/Decryption:** Encrypt and decrypt files with progress feedback.
- **Cryptographic Utilities:** Includes functions for HMAC, HKDF, PKCS7 padding, and basic XOR operations.

## Requirement
- Python 3.12.4+
- hashlib
- hmac

## Installation

This module is a standalone Python script. Ensure you have Python installed on your system to run this module.

## Usage

### Basic Encryption and Decryption

To encrypt or decrypt data, initialize an `AES` object with the desired key size and use the `encrypt` and `decrypt` methods. For file operations, use `encrypt_file` and `decrypt_file`.

```python
from aes_module import AES

# Create an AES object
aes = AES(key_size=256) # 128 and 192-bit key is also available.

# Encrypt data
encrypted_data = aes.encrypt(key=b'your-key-here', plain_text=b'Hello, World!', enc_mod='cbc') # ecb mode is also available.
 
# Decrypt data
decrypted_data = aes.decrypt(key=b'your-key-here', cipher_text=encrypted_data, enc_mod='cbc')
```

### File Encryption and Decryption

```python
# Encrypt a file
aes.encrypt_file(key=b'your-key-here', source_file='path/to/source.file', dest_file='path/to/dest.file.enc')

# Decrypt a file
aes.decrypt_file(key=b'your-key-here', source_file='path/to/encrypted.file.enc', dest_file='path/to/decrypted.file')
```

### Custom AES Encryption/Decryption Toolkit

``` python
from aes_module import AES, add_pkcs7_padding, remove_pkcs7_padding ,hkdf
aes_key_length = 128
aes = AES(aes_key_length)

key = b'My Super Death Key that kills'
data = b'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris eros ipsum, facilisis non neque eu, dapibus congue tortor.'
#Add PKCS#7 padding to ensure the data's length is a multiple of the AES block size (16 bytes).
padded_data = add_pkcs7_padding(data)

#Use HKDF to derive a secure key from the initial key, with the length specified by aes_key_length / 8.
derived_key = hkdf(key, aes_key_length//8, salt=b'',info=b'')

print(f'Data after padding : {padded_data}')
print(f'Derived key with hkdf : {derived_key.hex()}')

# Encrypt the data using AES in ECB mode. Note: ECB mode is generally not recommended for secure applications due to its vulnerability to certain attacks.
cipher_text = b''
#Process each 16-byte block of padded data.
for i in range(0, len(data), 16):
    # Encrypt each block individually.
    encrypted_block = aes.encrypt_block(derived_key, padded_data[i:i+16])
    cipher_text += encrypted_block
print(f'Encrypted data : {cipher_text.hex()}')

# Decrypt the data using AES in ECB mode.
padded_data = b''
#Process each 16-byte block of cipher text.
for i in range(0, len(cipher_text), 16):
    # Decrypt each block individually.
    decrypted_block = aes.decrypt_block(derived_key, cipher_text[i:i+16])
    padded_data += decrypted_block

print(f'Decrypted data : {padded_data}')
#Remove PKCS#7 padding to recover the original plaintext data.
recovered_data = remove_pkcs7_padding(padded_data)
print(f'Recovered data : {recovered_data}')
```

## Description of AES
Below is an excellent video on the AES function of **Computerphile** that you can watch.

[![Video Title](https://i3.ytimg.com/vi/O4xNJsjtN6E/hqdefault.jpg)](https://www.youtube.com/watch?v=O4xNJsjtN6E "AES explained (Advanced Encryption Standard) - Computerphile")

### AES Data Structure
AES is a variant of Rijndael, with a fixed block size of 128 bits, and a key size of 128, 192, or 256 bits. AES operates on a 4 × 4 column-major order array of 16 bytes $ \begin{pmatrix} b_0,b_1,b_2,... ,b_{15}\end{pmatrix} $ termed *"The state"*.

\[ \begin{pmatrix}
b_0 & b_4 & b_8 & b_{12} \\
b_1 & b_5 & b_9 & b_{13} \\
b_2 & b_6 & b_{10} & b_{14} \\
b_3 & b_7 & b_{11} & b_{15}
\end{pmatrix} \]


In this code we use function to convert bytes to matrix of 4 × 4 column-major of 1 byte each :

```python
    def bytes2matrix(self, data: bytes):
        # Convert a 16-byte array into a matrix format for easier manipulation during the AES algorithm.
        if len(data) not in (16, 24, 32):
            raise ValueError("Data must be 16, 24, or 32 bytes long")
        
        # Convert bytes to matrix
        return [list(data[i:i+4]) for i in range(0, len(data), 4)]

    def matrix2bytes(self, matrix : tuple):
        # Convert a matrix back into a byte array after processing is done.
        byte_array = []
        for row in matrix:
            for element in row:
                byte_array.append(element)
        return bytes(byte_array)
```

The AES algorithm consists of several steps, which can be broken down into key expansion and encryption processes.
The key size used for an AES cipher specifies the number of transformation rounds that convert the input, called the plaintext, into the final output, called the ciphertext. The number of rounds are as follows:

- 10 rounds for 128-bit keys.
- 12 rounds for 192-bit keys.
- 14 rounds for 256-bit keys.

Each round consists of several processing steps, including one that depends on the encryption key itself. A set of reverse rounds are applied to transform ciphertext back into the original plaintext using the same encryption key.


## AES Encryption Process
The AES encryption process includes several key stages, each of which involves specific transformations:

### Key Expansion
- **KeyExpansion**: Round keys are derived from the main cipher key using the AES key schedule algorithm.

### Initial Round
- **AddRoundKey**: The initial round key derived from the AES key schedule is combined with the state. This involves an XOR operation between each byte of the state and the round key.

### Main Rounds
Each main round includes the following steps, and is repeated 9, 11, or 13 times depending on the key length:
- **SubBytes**: A non-linear substitution step where each byte in the state is replaced with another according to a predefined lookup table.
- **ShiftRows**: A transposition step where each row of the state is shifted cyclically to the left.
- **MixColumns**: A mixing operation that transforms each column of the state.
- **AddRoundKey**: Each byte of the state is combined again with a byte of the round key using the XOR operation.

### Final Round
The final round consists of the following steps:
- **SubBytes**
- **ShiftRows**
- **AddRoundKey**

The final state is then converted back into the ciphertext block.


## AES Steps


### AddRoundKey

In the AddRoundKey step, each byte of the state is combined with a byte of the round subkey using the XOR operation.
In the AddRoundKey step, the subkey is combined with the state. For each round, a subkey is derived from the main key using Rijndael's key schedule (Expand Key step), each subkey is the same size as the state. The subkey is added by combining of the state with the corresponding byte of the subkey using bitwise XOR.

![In the AddRoundKey step, each byte of the state is combined with a byte of the round subkey using the XOR operation (⊕).](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/AES-AddRoundKey.svg/320px-AES-AddRoundKey.svg.png)

```python
    def add_round_key(self, s, k):
        # Perform the AddRoundKey step by XORing the state matrix with the round key matrix.
        for i in range(len(s)):
            for j in range(len(s[i])):
                s[i][j] = (s[i][j] ^ k[i][j])
        return s
```
### Expand key
The key expansion step in AES generates a series of round keys from the original cipher key. These round keys are then used in each round of the AES encryption process. The key expansion process is crucial for the security of AES, as it ensures that each round key is unique and derived from the original key in a complex manner.

<u>Rcon (Round Constant)</u> : A pre-defined array of round constants (Rcon) is used in the key expansion process. These constants are derived from a finite field and ensure non-linearity in the expanded keys.  You can see mot details on [Wikipedia AES key schedule](https://en.wikipedia.org/wiki/AES_key_schedule#Round_constants)

```python
    self.R_CON = (
            0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
            0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
            0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
            0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
        )

    def expand_key(self,master_key):
        # Expand the initial cipher key into several round keys for use in each round of the AES algorithm.
        key_columns = self.bytes2matrix(master_key)
        iteration_size = len(master_key) // 4
        i = 1
        while len(key_columns) < (self.n_rounds + 1) * 4:
            word = list(key_columns[-1])
            if len(key_columns) % iteration_size == 0:
                word.append(word.pop(0)) # Rotate the word
                word = [self.S_BOX[b] for b in word]  # Substitute using S_BOX
                word[0] ^= self.R_CON[i]  # XOR with round constant
                i += 1
            elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
                word = [self.S_BOX[b] for b in word]  # Only for 256-bit keys
            word = bytes(i^j for i, j in zip(word, key_columns[-iteration_size]))
            key_columns.append(word)

        return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]
```
### SubBytes 
The SubBytes step applies a non-linear substitution to each byte of the state matrix using a substitution box (S-box). This S-box is a precomputed lookup table that contains a permutation of all possible 256 8-bit values (0x00 to 0xFF).
![In the SubBytes step, each byte in the state is replaced with its entry in a fixed 8-bit lookup table, S; bij = S(aij).](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/AES-SubBytes.svg/320px-AES-SubBytes.svg.png)

```python
    self.S_BOX = (
            0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, ...)
        # INV_S_BOX is used for the inverse SubBytes step in the decryption process.
    self.INV_S_BOX = (
            0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, ...)

    def sub_bytes(self, s):
        # Substitute each byte in the state matrix with its corresponding byte in S_BOX.
        for i in range(len(s)):
            for j in range(len(s[i])):
                s[i][j] = self.S_BOX[s[i][j]]
        return s
    
    def inv_sub_bytes(self, s):
        # Substitute each byte in the state matrix with its corresponding byte in INV_S_BOX during decryption.
        for i in range(len(s)):
            for j in range(len(s[i])):
                s[i][j] = self.INV_S_BOX[s[i][j]]
        return s
```
### ShiftRows
The ShiftRows step operates on the rows of the state; it cyclically shifts the bytes in each row by a certain offset : 
- The first row is left unchanged
- The second row is shifted one to the left
- The third rows is shifted by offsets of two 
- The fourth rows is shifted by three

The importance of this step is to avoid the columns being encrypted independently, in which case AES would degenerate into four independent block ciphers.

![In the ShiftRows step, bytes in each row of the state are shifted cyclically to the left. The number of places each byte is shifted differs incrementally for each row.](https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/AES-ShiftRows.svg/320px-AES-ShiftRows.svg.png)
```python
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
```

### MixColumns 
The MixColumns step is one of the core transformations in the AES (Advanced Encryption Standard) encryption algorithm. It provides diffusion by mixing the bytes within each column of the state matrix. This step makes it so that a single byte change in the input results in changes to multiple bytes in the output, enhancing the security of the encryption process.


![In the MixColumns step, each column of the state is multiplied with a fixed polynomial](https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/AES-MixColumns.svg/320px-AES-MixColumns.svg.png)

$$ \begin{bmatrix} b_{0,1} \\ b_{1,1} \\ b_{2,1} \\ b_{3,1} \end{bmatrix} = \begin{bmatrix} 2 & 3 & 1 & 1 \\ 1 & 2 & 3 & 1 \\1 & 1 & 2 & 3 \\3 & 1 & 1 & 2 \end{bmatrix}  \begin{bmatrix} a_{0,1} \\ a_{1,1} \\ a_{2,1} \\ a_{3,1} \end{bmatrix}$$



``` python
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
```

## Source Acknowledgment
This module incorporates significant contributions from the educational resources available on [Cryptohack](https://cryptohack.org/courses/symmetric/course_details/), an excellent platform for learning about cryptographic techniques. Additionally, parts of this code were developed with the assistance of ChatGPT-4, leveraging its capabilities to enhance functionality and ensure clarity in implementation. Furthermore, this project also references information from [Wikipedia](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard), the free encyclopedia, to provide comprehensive and reliable data on various cryptographic concepts and algorithms.

## License

This project is open-sourced under the MIT license.

---

Feel free to adjust the sections according to your project's needs, such as adding a section for requirements or more detailed instructions on how to set up the environment.
