
# RSA Encryption Algorithm Implementation in Python

This Python codebase implements the Rivest-Shamir-Adleman (RSA) encryption algorithm. It supports various key sizes, with the default being 512 bits. The primary purpose of this implementation is to facilitate educational and testing activities, allowing users to explore and understand the core concepts of RSA encryption.

## Important Notice
**This implementation is intended for educational and testing purposes only.** Please refrain from using this code in real-world projects or production environments.

Before using this code, I recommend studying RSA. At the end of this readme, you can find an explanation about RSA.

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

### Key Generation

To generate RSA keys, begin by randomly selecting two large prime numbers, denoted as $p$ and $q$. It's crucial that $p$ and $q$ are significantly different to mitigate certain cryptographic attacks.

Next, compute the modulus $n$ by multiplying $p$ and $q$:
$n = p \times q$

The next step involves computing $\lambda(n)$, where $\lambda(n)$ is  [Carmichael's totient function](https://en.wikipedia.org/wiki/Carmichael_function). Since $n = pq$, $\lambda(n) = \text{lcm}(\lambda(p), \lambda(q))$. 
However, for simplicity,  if $p$ and $q$ are distinct primes, $\lambda(n)$ can also be computed as :
$\lambda(n) = (p-1) \times (q-1)$
(For additional details, refer to [RSA Cryptosystem on Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem))).

Following this, select a number $e$ that is [coprime](https://en.wikipedia.org/wiki/Coprime_integers) to $\lambda(n)$  and satisfies $1 < e< \lambda(n)$. A common choice for $e$ is $65537$ due to its properties that favor efficient computation. This number is referred to as the public exponent.

Lastly, compute a number $d$, which is the modular [modular multiplicative inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse) of $e$ modulo $\lambda(n)$ :
$d \equiv e^{-1} \pmod{\lambda(n)}$.
The [extended Euclidean algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm) is typically used to compute $d$. This number is referred to as the private exponent.

So, to summarize the RSA key generation process:
- Generate $p$ and $q$, two large prime numbers.
- Compute $n = p \times q$, which serves as the modulus.
- Compute  $\lambda(n) = (p-1) \times (q-1)$.
- Select e = 65537$, commonly chosen as the public exponent.
- Compute $d \equiv e^{-1} \pmod{\lambda(n)}$, which is the private exponent.

```python
# Generate two valid prime numbers of the given key size.
self.prime1, self.prime2 = find_valid_prime_pair(self.key_size)

# Compute the modulus n = p * q.
self.modulus = self.prime1 * self.prime2

# Compute Euler's totient phi(n) = (p - 1) * (q - 1).
phi = (self.prime1 - 1) * (self.prime2 - 1)

self.public_exponent = 65537

# Calculate the private exponent d as the modular inverse of the public exponent.
self.private_exponent = pow(self.public_exponent, -1, phi)
```

### Public and Private Keys:

- The **public key** consists of the pair $(e, n)$. This key can be distributed openly to anyone.
- The **private key** consists of the pair $(d, n)$. This key must remain absolutely confidential.

### Encryption / Decryption

#### Encryption :
To encrypt data $M$, you must first convert it to a number $m$. If the data is text, for example, you can use UTF-8 encoding (for example, 'Hello, RSA!' can be represented as 87521618088895491219865889).

**Note:** The number $m$ must be less than $n$, otherwise, the calculation will be compromised.

To encrypt the data, you will need the public key $(e, n)$ and compute:
$c \equiv m^e \pmod{n}$.

```python
# Convert text to an integer representation.
int_text = convert_to_int(text)

# Encrypt: ciphertext = (message^public_exponent) mod modulus.
encrypted_int = pow(int_text, public_exponent, modulus)
```

#### Decryption :
To decrypt $c$, you will need the private key $(d, n)$ and compute:
$m \equiv c^d \pmod{n}$.
To recover the original information, convert the number $m$ $ back into the data $M$.

```python
# Decrypt: message = (ciphertext^private_exponent) mod modulus.
decrypted_int = pow(encrypted_int, self.private_exponent, self.modulus)

# Convert the integer back to text.
decrypted_text = convert_to_text(decrypted_int)
```

### Digital Signature / Signature Verification

#### Digital signature 
To sign data, you will need $(d, n)$. Additionally, you'll use a hash function such as SHA-256.

First, compute the hash of the data using a hash function:
$ h = Hash(m)$.

Then compute the signature $s$ using the private exponent : $s \equiv h^d \pmod{n}$..

The signature is now composed of the pair $(s, m)$.


```python
# Compute the SHA-256 hash of the text and convert it to an integer.
hash_int = int(sha256(text.encode('utf-8')).hexdigest(), 16)

# Sign: signature = (hash^private_exponent) mod modulus.
signature = pow(hash_int, self.private_exponent, self.modulus)
```
#### Signature Verification
To verify the signature, you need to compute the hash of the message again: $ h = Hash(m)$.

But this time, compute $h'$ using the public exponent : $h' \equiv s^e \pmod{n}$. 

If $h' = h$, then the signature is valid.


```python
# Compute the hash of the original text.
hash_int = int(sha256(text.encode('utf-8')).hexdigest(), 16)

# Decrypt the signature: decrypted_signature = (signature^public_exponent) mod modulus.
decrypted_signature = pow(signature, public_exponent, modulus)

# The signature is valid if the decrypted signature equals the hash.
return hash_int == decrypted_signature
```
## Source Acknowledgment
This module incorporates significant contributions from the educational resources available on [CryptoHack](https://cryptohack.org/courses/public-key/course_details/), an excellent platform for learning about cryptographic techniques. Additionally, parts of this code were developed with the assistance of ChatGPT, leveraging its capabilities to enhance functionality and ensure clarity in implementation. Furthermore, this project also references information from [Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem)), the free encyclopedia, to provide comprehensive and reliable data on various cryptographic concepts and algorithms.

## License

This project is open-sourced under the MIT license.

---

Feel free to adjust the sections according to your project's needs, such as adding a section for requirements or more detailed instructions on how to set up the environment.