# ML-DSA in a nutshell! (toy version: small vectors instead of real polynomial rings)
import random, hashlib

# --- Public parameters ---
q = 8380417      # modulus (the real ML-DSA prime, kept for flavor)
n = 4            # vector dimension (real ML-DSA: hundreds of dims worth of polynomial coeffs)
eta = 2          # secret coefficients live in [-eta, eta] — "small" is the whole point
gamma1 = 1 << 17 # bound for the random masking vector y
beta = 78        # if z grows past this, we abort and retry (rejection sampling)

def rand_vec(bound, size=n):
    return [random.randint(-bound, bound) for _ in range(size)]

def rand_matrix(rows, cols):
    return [[random.randint(0, q - 1) for _ in range(cols)] for _ in range(rows)]

def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) % q for i in range(len(A))]

def vec_add(a, b): return [(x + y) % q for x, y in zip(a, b)]
def vec_sub(a, b): return [(x - y) % q for x, y in zip(a, b)]
def scalar_mul(c, v): return [(c * x) % q for x in v]

# Real ML-DSA hashes only the HIGH-order bits of w (drops low bits) so that
# the small c·s2 error in Verify doesn't change the hash. We fake that with rounding.
def high_bits(v, r=64):
    return tuple(((x + r // 2) % q) // r for x in v)

def challenge(message, w):
    data = str((message, high_bits(w))).encode()
    return int(hashlib.sha256(data).hexdigest(), 16) % 4  # tiny challenge space, for demo only

# --- KeyGen ---
A = rand_matrix(n, n)            # public matrix (real ML-DSA derives this from a public seed)
s1 = rand_vec(eta)               # secret vector 1
s2 = rand_vec(eta)               # secret vector 2 (the "error")
t = vec_add(matvec(A, s1), s2)   # public key value: t = A·s1 + s2

public_key = (A, t)
private_key = (s1, s2)
print("Public key t:", t)
print("Private key (s1, s2):", private_key)

# --- Alice and Bob example ---
message = "Hello Bob"

# Alice signs: mask with y, hash to get challenge c, combine with secret -> z
def sign(message, s1, A):
    while True:
        y = rand_vec(gamma1)               # fresh random mask each attempt
        w = matvec(A, y)                   # commitment
        c = challenge(message, w)          # ties signature to the message
        z = vec_add(y, scalar_mul(c, s1))  # response using the secret

        if max(abs(x) for x in z) < gamma1 - beta:
            return z, c
        # else: z leaked too much about s1 -> abort, loop again (RSA never needs this step)

z, c = sign(message, s1, A)
print("Alice sends message:", message)
print("Alice sends signature (z, c):", (z, c))

# Bob verifies: recompute w from z and the PUBLIC key, check the hash matches
def verify(message, z, c, A, t):
    if max(abs(x) for x in z) >= gamma1 - beta:
        return False
    w_check = vec_sub(matvec(A, z), scalar_mul(c, t))  # = A·y - c·s2  (close to original w)
    return challenge(message, w_check) == c

if verify(message, z, c, A, t):
    print("Valid signature — this really came from Alice!")
else:
    print("Invalid signature — reject this message!")