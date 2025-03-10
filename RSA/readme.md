# RSA Encryption Algorithm Implementation in Python

This Python codebase implements the Rivest-Shamir-Adleman (RSA) encryption algorithm. It supports various key sizes, with the default being 512 bits. The primary purpose of this implementation is to facilitate educational and testing activities, allowing users to explore and understand the core concepts of RSA encryption.

## Important Notice
**This implementation is intended for educational and testing purposes only.** Please refrain from using this code in real-world projects or production environments.

Before using this code, I recommend you study RSA. At the end of this readme, you can find an explanation about RSA.

## Features

- **Key Size Support:** Customizable key sizes.
- **Data Encryption/Decryption:** Encrypt and decrypt small messages directly with RSA.
- **Digital Signature:** Sign messages and verify signatures to authenticate message integrity and source.
- **Key Generation:** Generate and manage RSA key pairs.

## Requirements
- Python 3.9+
- PyCryptoDome (optional for enhanced features)

## Installation

This module is a standalone Python script. Ensure you have Python installed on your system to run this module.


## Usage
This section demonstrates how to use the RSA module to perform encryption and decryption, as well as how to view key information.

### Initializing and Viewing RSA Key Information
First, create an RSA object with a specified key size. Printing the RSA object will display all relevant key information:
```python
from rsa_module import RSA

# Create an RSA object with a specific key size
rsa = RSA(key_size=512)  # In real usage, a key size of 2048 bits is recommended.

# Display the RSA key information
print(rsa)
```

### Encryption and Decryption
Encrypt and decrypt messages using RSA to demonstrate public-key cryptography:
```python
from rsa_module import RSA

# Create an RSA object with a specific key size
rsa = RSA(key_size=512)  # In real usage, a key size of 2048 bits is recommended.

# Export public key
public_key = (rsa.modulus, rsa.public_exponent)

# Encrypt data with the public key only (we don't need the original RSA object)
encrypted_message = RSA.encrypt(None, 'Hello, RSA!', *public_key)
print("Encrypted Message:", encrypted_message)

# Decrypt the message using the private key
decrypted_message = rsa.decrypt(encrypted_message)
print("Decrypted Message:", decrypted_message)
```

### Digital Signatures
Generate and verify digital signatures to authenticate messages:
```python

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
```

## Description of RSA

### Key generation

For generate key you must fisrt generate randomly two large primes numbers that we call p an q (the two primes must be large difference to prevent some attacks).

Secondly you just need to multiply those two number and get the result as n, we will call this number n the modulus :
$n = p \times q$

Now we will need **λ(n)**, where λ is [Carmichael's totient function](https://en.wikipedia.org/wiki/Carmichael_function), but since p and q are prime we juste need to compute $\lambda(n) = (p-1) \times (q-1)$ (if u need more details go check : [RSA_(cryptosystem)](https://en.wikipedia.org/wiki/RSA_(cryptosystem))).


Next we will need a number **e** [coprime](https://en.wikipedia.org/wiki/Coprime_integers) with $\lambda(n)$ such as  $1 < e < \lambda(n)$, we will call this number the public exponent. (this number is often 65537)

And finally we juste to find d such as d is the modular [modular multiplicative inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse) of e modulo λ(n), in math language : *$d \equiv e^{-1} \pmod{\lambda(n)}$*. We can easily find d with the [extended Euclidean algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm). We will call tha number the private exponent





## Source Acknowledgment
This module incorporates significant contributions from the educational resources available on [CryptoHack](https://cryptohack.org/courses/public-key/course_details/), an excellent platform for learning about cryptographic techniques. Additionally, parts of this code were developed with the assistance of ChatGPT, leveraging its capabilities to enhance functionality and ensure clarity in implementation. Furthermore, this project also references information from [Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem)), the free encyclopedia, to provide comprehensive and reliable data on various cryptographic concepts and algorithms.

## License

This project is open-sourced under the MIT license.

---

Feel free to adjust the sections according to your project's needs, such as adding a section for requirements or more detailed instructions on how to set up the environment.

