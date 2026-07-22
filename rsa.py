# RSA in a nutshell

import hashlib
import random

from collections.abc import Callable


# n is the modulus — same role Q plays in ML-DSA. Every number lives mod n
# so values stay bounded, but here n is a secret-sized product of two huge
# primes (not a small public constant) — that's the whole security model.
KEY_BITS = 512

# Public exponent — almost always 65537. It's prime, small enough for fast
# verification (pow(x, E, n) is cheap), and has enough set bits to resist a
# handful of textbook attacks on tiny/weak exponents.
PUBLIC_EXPONENT = 65537  # https://en.wikipedia.org/wiki/65,537


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


def random_candidate(bits: int = KEY_BITS) -> int:
    return random.getrandbits(bits) | 1


def generate_prime(generator: Callable[[], int]) -> int:
    while True:
        n = generator()
        if is_prime(n):
            return n


# Real RSA security rests on factoring n back into p and q being infeasible
# — that's the "hard problem" here, the same role the lattice problem plays
# for ML-DSA. d is the modular inverse of E, so it only exists because we
# know phi = (p-1)(q-1); an attacker who can't factor n can't compute phi
# and can't derive d from E either.
def key_generation() -> dict:
    # Pick two large random primes p, q
    p = generate_prime(random_candidate)
    q = generate_prime(random_candidate)

    n = p * q

    # Compute Euler's totient φ(n) = (p-1)(q-1).
    phi = (p - 1) * (q - 1)

    E = PUBLIC_EXPONENT
    d = pow(E, -1, phi)

    return {"public": (n, E), "private": (n, d)}


def sign(message: str, private_key: tuple) -> int:
    n, d = private_key
    digest = hashlib.sha256(message.encode()).digest()  # bytes
    message_hash = int.from_bytes(digest, "big")  # -> int

    # signature = hash(message)^d mod n — only the private-key holder can
    # compute this, since only they know d.
    return pow(message_hash, d, n)


def verify(message: str, signature: int, public_key: tuple) -> bool:
    n, E = public_key
    # Undo the signature with the public exponent: sig^E mod n = hash^(d*E)
    # mod n = hash mod n, because d and E are inverses mod phi(n).
    recovered = pow(signature, E, n)
    digest = hashlib.sha256(message.encode()).digest()
    message_hash = int.from_bytes(digest, "big")
    return message_hash == recovered


if __name__ == "__main__":
    keys = key_generation()
    public_key = keys["public"]
    private_key = keys["private"]
    n, E = public_key

    # --- Alice and Bob example ---
    message = "Hello Bob"

    print("Public key (n, E):", public_key)
    print("Private key (n, d):", private_key)

    signature = sign(message, private_key)
    print("Alice sends message:", message)
    print("Alice sends signature:", signature)

    if verify(message, signature, public_key):
        print("Valid signature — this really came from Alice!")
    else:
        print("Invalid signature — reject this message!")
