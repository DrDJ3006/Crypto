import numpy as np

def generate_lattice_basis(dim, noise_level=0):
    """ Generate a robust lattice basis with reduced noise. """
    while True:
        Q, _ = np.linalg.qr(np.random.randn(dim, dim))
        perturbation = np.random.randn(dim, dim) * noise_level
        basis = np.round(Q + perturbation).astype(int)
        if np.linalg.det(basis) != 0:
            return basis

def generate_private_key(dim):
    return generate_lattice_basis(dim, noise_level=0.005)  # Reduced noise level for better orthogonality

def generate_public_key(private_key):
    while True:
        transformation = generate_lattice_basis(private_key.shape[0], noise_level=1.5)
        public_key = np.dot(private_key, transformation)
        if np.linalg.det(public_key) != 0:
            return public_key

def encrypt(message_vector, public_key):
    return np.dot(message_vector, public_key)

def decrypt(ciphertext, private_key):
    """ Use a more robust rounding strategy in decryption. """
    approx_message = np.dot(ciphertext, np.linalg.inv(private_key))
    return np.round(approx_message).astype(int)  # More direct rounding

def string_to_vector(s):
    return np.array([ord(c) for c in s])

def vector_to_string(v):
    """ Safe conversion to string, ignoring non-ASCII values. """
    chars = []
    for n in v:
        if 0 <= n <= 127:  # Only convert ASCII-range integers
            chars.append(chr(n))
        else:
            chars.append('?')  # Placeholder for out-of-range values
    return ''.join(chars)

# Example usage
dim = 8
private_key = generate_private_key(dim)
public_key = generate_public_key(private_key)

message = "OpenAI G"
message_vector = string_to_vector(message)
ciphertext = encrypt(message_vector, public_key)

decrypted_vector = decrypt(ciphertext, private_key)
decrypted_message = vector_to_string(decrypted_vector)

print("Original message:", message)
print("Message vector:", message_vector)
print("Ciphertext:", ciphertext)
print("Decrypted vector:", decrypted_vector)
print("Decrypted message:", decrypted_message)
