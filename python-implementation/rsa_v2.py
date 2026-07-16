import hashlib
from generate_primes import generate_prime


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
