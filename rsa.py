import hashlib
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


def key_generation() -> dict:
    # Pick two large random primes p, q
    p = generate_prime()
    q = generate_prime()

    n = p * q

    # Compute Euler's totient φ(n) = (p-1)(q-1).
    phi = (p - 1) * (q - 1)

    # Choose public exponent e — almost always 65537
    E = 65537  # https://en.wikipedia.org/wiki/65,537
    d = pow(E, -1, phi)

    return {"public": (n, E), "private": (n, d)}


def sign(message: str, private_key: tuple) -> int:
    n, d = private_key
    digest = hashlib.sha256(message.encode()).digest()  # bytes
    message_hash = int.from_bytes(digest, "big")  # -> int
    return pow(message_hash, d, n)


def verify(message: str, signature: int, public_key: tuple) -> bool:
    n, E = public_key
    recovered = pow(signature, E, n)
    digest = hashlib.sha256(message.encode()).digest()
    message_hash = int.from_bytes(digest, "big")
    return message_hash == recovered
