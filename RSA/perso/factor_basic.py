import random

def is_probably_prime(n, k=10):
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
    
def factors(x):
    # We will store all factors in `result`
    result = []
    n=x
    for i in range(2,x):
        if n%i==0:
            result.append(i)
            print(i)
            n=n//i
            factors(n)
        if is_probably_prime(n):
            exit()
    return result

print(factors(170799023429782709819859295362059365939))