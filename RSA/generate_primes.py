import random

def is_prime(n, k=5):
    """Check if a number is prime using the Miller-Rabin test with k iterations."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Find r and d such that n-1 = 2^r * d with d being odd
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Perform k rounds of the Miller-Rabin test
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # Compute a^d % n
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite number
    return True  # Probably prime

def generate_prime(n_bits):
    """Generate an n-bit prime number using only random."""
    while True:
        num = random.getrandbits(n_bits)  # Generate a random number with n bits
        num |= (1 << (n_bits - 1)) | 1  # Ensure the number is odd and has the highest bit set
        if is_prime(num):
            return num

def find_valid_prime_pair(key_bits_size):
    """
    Generate two prime numbers p and q such that their product has exactly key_bits_size bits.
    """
    while True:
        # Calculate half the key size for p and q
        half_bits = key_bits_size // 2

        # Generate p and q with slight bit variations to ensure exact key size
        p = generate_prime(half_bits)
        q = generate_prime(key_bits_size - half_bits)

        product = p * q
        product_bits = product.bit_length()

        # Ensure p * q has exactly key_bits_size bits
        if product_bits == key_bits_size:
            return p, q

        # If product is too small, slightly increase q's bit size
        if product_bits < key_bits_size:
            q = generate_prime(key_bits_size - half_bits + 1)

        # If product is too large, slightly decrease q's bit size
        if product_bits > key_bits_size:
            q = generate_prime(key_bits_size - half_bits - 1)