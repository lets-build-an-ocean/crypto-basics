# ML-DSA in a nutshell

import random
import hashlib


from collections.abc import Callable


def create_matrix(rows: int, cols: int, generator: Callable[[], int]):
    return [[generator() for _ in range(cols)] for _ in range(rows)]


# We use this function to fill the items in matrix
# Q is the modulus — same role n plays in RSA. Every number lives mod Q so
# values stay small and wrap around instead of growing without bound.

Q = 17


def random_integer(Q=17) -> int:
    return random.randrange(Q)


"""
ML DSA starts with a matrix if polynomials but for simplicity we use a matrix of integers
ML-DSA Variant	Matrix size
ML-DSA-44	4 × 4
ML-DSA-65	5 × 6
ML-DSA-87	7 × 8

Notice these are actually quite small matrices.
People are often surprised because they expect something like 1000×1000.
"""


def generate_secret_vector(size: int) -> list[int]:
    # TODO: Use better bound/eta here
    return [random.choice([-1, 0, 1]) for _ in range(size)]


def matrix_vector_multiply(matrix: list[list[int]], vector: list[int]) -> list[int]:
    result = []

    # Process one row at a time.
    for row in matrix:
        row_result = 0

        # Compute the dot product of the row and the vector.
        for matrix_value, vector_value in zip(row, vector):
            row_result += matrix_value * vector_value

        result.append(row_result % Q)

    return result


def vector_add(a: list[int], b: list[int]) -> list[int]:
    return [(x + y) % Q for x, y in zip(a, b)]


def vector_sub(a: list[int], b: list[int]) -> list[int]:
    return [(x - y) % Q for x, y in zip(a, b)]


def scalar_vector_multiply(c: int, v: list[int]) -> list[int]:
    return [(c * x) % Q for x in v]


# A is Public matrix used by everyone during key generation,
# signing, and verification.
ROWS = 4
COLUMNS = 4


# Real ML-DSA sets t = A·s1 + s2, mixing in a small error vector s2 — that
# error is what makes the underlying math problem lattice-hard. It also means
# the verifier can only rebuild an APPROXIMATE w, so real ML-DSA hashes only
# the high bits of w to hide that tiny mismatch. Both pieces (s2, high-bit
# rounding) add real complexity for a small conceptual win here, so this demo
# drops them: t = A·s1 (no error), verify rebuilds w exactly. See ml-dsa.py
# for the version with the error term and rounding included.
def key_generation() -> dict:
    A = create_matrix(ROWS, COLUMNS, random_integer)
    s1 = generate_secret_vector(COLUMNS)
    t = matrix_vector_multiply(A, s1)

    return {"public": (A, t), "private": s1}


def hash_to_challenge(message: str, w: list[int]) -> int:
    # Kept tiny (1..3) on purpose. Real ML-DSA uses a huge challenge space
    # via low-weight polynomials; a 3-value space here is NOT secure.
    data = message.encode() + b"|" + ",".join(map(str, w)).encode()
    return 1 + hashlib.sha256(data).digest()[0] % 3


def sign(message: str, private_key: list[int], A: list[list[int]]):
    s1 = private_key
    y = [random_integer() for _ in range(COLUMNS)]  # masking vector
    w = matrix_vector_multiply(A, y)  # commitment  w = A·y
    c = hash_to_challenge(message, w)  # challenge
    z = vector_add(y, scalar_vector_multiply(c, s1))  # response    z = y + c·s1
    return z, c


def verify(message: str, signature: tuple, public_key: tuple) -> bool:
    A, t = public_key
    z, c = signature

    # A·z - c·t = A·y + c·A·s1 - c·A·s1 = A·y = w, exactly (no error to hide).
    # The verifier never sees s1 or y — it rebuilds w from public data only,
    # then checks it hashes to the same challenge.
    w_check = vector_sub(matrix_vector_multiply(A, z), scalar_vector_multiply(c, t))
    return hash_to_challenge(message, w_check) == c


if __name__ == "__main__":
    keys = key_generation()
    public_key = keys["public"]
    private_key = keys["private"]
    A, t = public_key

    # --- Alice and Bob example ---
    message = "Hello Bob"

    print("Public key t:", t)
    print("Private key s1:", private_key)

    signature = sign(message, private_key, A)
    print("Alice sends message:", message)
    print("Alice sends signature (z, c):", signature)

    if verify(message, signature, public_key):
        print("Valid signature — this really came from Alice!")
    else:
        print("Invalid signature — reject this message!")
