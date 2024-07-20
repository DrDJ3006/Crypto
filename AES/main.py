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




