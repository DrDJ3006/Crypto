import random
import sys
def is_probably_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if num % 2 == 0:
            num += 1
        if is_probably_prime(num):
            return num

nNumbits=int(sys.argv[1])
prime1 = generate_prime(int(nNumbits/2))
prime2 = generate_prime(int(nNumbits/2))
product=prime1*prime2
while int(product).bit_length() != nNumbits:
    prime1 = generate_prime(int(nNumbits/2))
    prime2 = generate_prime(int(nNumbits/2))
    product=prime1*prime2
print(f'q = {prime1} : {int(prime1).bit_length()} bits')
print(f'p = {prime2} : {int(prime2).bit_length()} bits')
print(f'n = {product} : {int(product).bit_length()} bits')