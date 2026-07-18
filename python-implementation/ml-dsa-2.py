# ML-DSA in a nutshell

import random


from collections.abc import Callable

def create_matrix(
    rows: int,
    cols: int,
    generator: Callable[[], int]
):
    return [
        [generator() for _ in range(cols)]
        for _ in range(rows)
    ]

# We use this function to fill the items in matrix
# TODO: What is Q?
def random_integer(Q = 17) -> int:
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
    return [
        random.choice([-1, 0, 1])
        for _ in range(size)
    ]


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

# A is Public matrix used by everyone during key generation,
# signing, and verification.
ROWS = 4
COLUMNS = 4
A = create_matrix(ROWS, COLUMNS, random_integer)
s = generate_secret_vector(COLUMNS)

t = matrix_vector_multiply(A, s)

public_key = (A, t)
private_key = s



