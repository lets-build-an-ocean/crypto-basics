# ML-DSA in a nutshell

import random


from collections.abc import Callable


def create_matrix(rows: int, cols: int, generator: Callable[[], int]):
    return [[generator() for _ in range(cols)] for _ in range(rows)]


# We use this function to fill the items in matrix
# TODO: What is Q?

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
            # row_result = (row_result + matrix_value * vector_value) % Q

        result.append(row_result)

    return result


def vector_add(a: list[int], b: list[int]) -> list[int]:
    return [(x + y) % Q for x, y in zip(a, b)]


# A is Public matrix used by everyone during key generation,
# signing, and verification.
ROWS = 4
COLUMNS = 4
A = create_matrix(ROWS, COLUMNS, random_integer)
s1 = generate_secret_vector(COLUMNS)
s2 = generate_secret_vector(ROWS)

t = vector_add(matrix_vector_multiply(A, s1), s2)

public_key = (A, t)
private_key = (s1, s2)


def hash_to_challenge(message: str, w: list[int]) -> int:
    import hashlib

    # Kept tiny (1..3) on purpose: it forces c*s2 to stay SMALL, which is the
    # whole point of the next version. Real ML-DSA uses a huge challenge space
    # via low-weight polynomials; a 3-value space here is NOT secure.
    data = message.encode() + b"|" + ",".join(map(str, w)).encode()
    return 1 + hashlib.sha256(data).digest()[0] % 3


def sign(message: str, private_key, A):
    s1, s2 = private_key
    y = [random_integer() for _ in range(COLUMNS)]  # masking vector
    w = matrix_vector_multiply(A, y)  # commitment  w = A·y
    c = hash_to_challenge(message, w)  # challenge
    z = vector_add(y, scalar_vector_multiply(c, s1))  # response    z = y + c·s1
    # w is returned ONLY so we can visualise the gap. It is NOT part of a real
    # signature — the verifier rebuilds its own copy from public data.
    return (z, c), w
