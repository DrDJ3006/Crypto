from generate_primes import find_valid_prime_pair
from hashlib import sha256

def convert_to_int(text):
    """
    Convert a string to an integer using UTF-8 encoding.
    """
    return int.from_bytes(text.encode('utf-8'), byteorder='big')

def convert_to_text(number):
    """
    Convert an integer back to a string using UTF-8 encoding.
    """
    num_bytes = (number.bit_length() + 7) // 8  # Calculate the number of bytes needed.
    return number.to_bytes(num_bytes, byteorder='big').decode('utf-8')

class RSA:
    def __init__(self, key_size, public_exponent=65537):
        """
        Initialize RSA by generating two primes, computing the modulus,
        Euler's totient (phi), and the private exponent.
        
        Args:
            key_size (int): The bit-size of the prime numbers.
            public_exponent (int): The public exponent (default is 65537).
        """
        self.key_size = key_size
        self.public_exponent = public_exponent
        
        # Generate two valid prime numbers of the given key size.
        self.prime1, self.prime2 = find_valid_prime_pair(self.key_size)
        
        # Compute the modulus n = p * q.
        self.modulus = self.prime1 * self.prime2
        
        # Compute Euler's totient phi(n) = (p - 1) * (q - 1).
        phi = (self.prime1 - 1) * (self.prime2 - 1)
        
        # Calculate the private exponent d as the modular inverse of the public exponent.
        self.private_exponent = pow(self.public_exponent, -1, phi)

    def __str__(self):
        """
        Return a string representation of the RSA key information.
        """
        return (
            f"RSA Key Information:\n"
            f"  Key Size: {self.key_size} bits\n"
            f"  Prime 1: {self.prime1}\n"
            f"  Prime 2: {self.prime2}\n"
            f"  Modulus: {self.modulus}\n"
            f"  Public Exponent: {self.public_exponent}\n"
            f"  Private Exponent: {self.private_exponent}\n"
        )

    def encrypt(self, text, modulus, public_exponent=65537):
        """
        Encrypt a text message using the public key.
        
        Args:
            text (str): The message to encrypt.
            modulus (int): The RSA modulus.
            public_exponent (int): The public exponent (default is 65537).
        
        Returns:
            int: The encrypted message as an integer.
        
        Raises:
            ValueError: If the integer representation of the text is not smaller than the modulus.
        """
        # Convert text to an integer representation.
        int_text = convert_to_int(text)
        if int_text >= modulus:
            raise ValueError("The integer representation of the text must be less than the modulus.")
        
        # Encrypt: ciphertext = (message^public_exponent) mod modulus.
        encrypted_int = pow(int_text, public_exponent, modulus)
        
        return encrypted_int


    def decrypt(self, encrypted_int):
        """
        Decrypt an integer message using the private key.
        
        Args:
            encrypted_int (int): The encrypted message as an integer.
        
        Returns:
            str: The decrypted text message.
        """
        # Decrypt: message = (ciphertext^private_exponent) mod modulus.
        decrypted_int = pow(encrypted_int, self.private_exponent, self.modulus)
        # Convert the integer back to text.
        decrypted_text = convert_to_text(decrypted_int)
        return decrypted_text

    def sign(self, text):
        """
        Sign a text message by signing its SHA-256 hash with the private key.
        
        Args:
            text (str): The message to sign.
        
        Returns:
            int: The digital signature as an integer.
        """
        # Compute the SHA-256 hash of the text and convert it to an integer.
        hash_int = int(sha256(text.encode('utf-8')).hexdigest(), 16)
        # Sign: signature = (hash^private_exponent) mod modulus.
        signature = pow(hash_int, self.private_exponent, self.modulus)
        return signature

    def verify_signature(self, text, signature, modulus, public_exponent=65537):
        """
        Verify a digital signature using the public key.
        
        Args:
            text (str): The original message.
            signature (int): The digital signature to verify.
        
        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        # Compute the hash of the original text.
        hash_int = int(sha256(text.encode('utf-8')).hexdigest(), 16)
        # Decrypt the signature: decrypted_signature = (signature^public_exponent) mod modulus.
        decrypted_signature = pow(signature, public_exponent, modulus)
        # The signature is valid if the decrypted signature equals the hash.
        return hash_int == decrypted_signature