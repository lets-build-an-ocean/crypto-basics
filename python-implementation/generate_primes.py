import random

def is_prime(n, k=10):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13]:
        if n % p == 0:
            return n == p

    r, d = 0, n - 1
    while d % 2 == 0:
        r, d = r + 1, d // 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        if all(pow(x, 2, n) != n - 1 for _ in range(r - 1)):
            return False
    return True

def generate_prime(bits=512):
    while True:
        n = random.getrandbits(bits) | 1
        if is_prime(n):
            return n