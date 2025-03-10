from rsa_module import RSA

# Create an RSA object with a specific key size
rsa = RSA(key_size=512)  # In real usage, a key size of 2048 bits is recommended.

# Export public key
public_key = (rsa.modulus, rsa.public_exponent)

# Sign a message
signature = rsa.sign('Hello, RSA!')
print("Signature:", signature)

# Verify the signature
is_valid = rsa.verify_signature('Hello, RSA!', signature, *public_key)
print("Signature Valid:", is_valid)