# AES Encryption Algorithm Implementation in Python

This Python codebase implements the Advanced Encryption Standard (AES) encryption algorithm. It supports key sizes of 128, 192, and 256 bits. The primary purpose of this implementation is to facilitate educational and testing activities, allowing users to explore and understand the core concepts of AES encryption.

## Important Notice
**This implementation is intended for educational and testing purposes only.** Please refrain from using this code in real-world projects or production environments.


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
from aes_module import Aes  # Ensure the script is appropriately named or adjusted for import

# Create an AES object
aes = Aes(key_size=256) # 128 and 192-bit key is also available.

# Encrypt data
encrypted_data = aes.encrypt(key=b'your-key-here', plain_text=b'Hello, World!', enc_mod='cbc') # ecb mode is also available.
 
# Decrypt data
decrypted_data = aes.decrypt(key=b'your-key-here', cipher_text=encrypted_data, enc_mod='cbc')
```

### File Encryption and Decryption

```python
# Encrypt a file
aes.encrypt_file(key=b'your-file-key', source_file='path/to/source.file', dest_file='path/to/dest.file.enc')

# Decrypt a file
aes.decrypt_file(key=b'your-file-key', source_file='path/to/encrypted.file.enc', dest_file='path/to/decrypted.file')
```

### Custom AES Encryption Toolkit

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

## Source Acknowledgment
This module incorporates significant contributions from the educational resources available on [Cryptohack](https://cryptohack.org/courses/symmetric/course_details/), an excellent platform for learning about cryptographic techniques. Additionally, parts of this code were developed with the assistance of ChatGPT-4, leveraging its capabilities to enhance functionality and ensure clarity in implementation.


## License

This project is open-sourced under the MIT license.

---

Feel free to adjust the sections according to your project's needs, such as adding a section for requirements or more detailed instructions on how to set up the environment.