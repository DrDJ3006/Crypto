from rsa_module import RSA

# Create an RSA object with a specific key size
rsa = RSA(key_size=128)  # In real usage, a key size of 2048 bits is recommended.

print(rsa)
# Export public key
public_key = (rsa.modulus, rsa.public_exponent)

# Encrypt data with the public key only (we don't need the original RSA object)
encrypted_message = RSA.encrypt(None, 'Hello, RSA!', *public_key)
print("Encrypted Message:", encrypted_message)

# Decrypt the message using the private key
decrypted_message = rsa.decrypt(encrypted_message)
print("Decrypted Message:", decrypted_message)