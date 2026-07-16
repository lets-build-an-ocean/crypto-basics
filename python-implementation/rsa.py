# RSA in a nutshell !

# Pick two large random primes p, q (e.g. 1024 bits each for a 2048-bit key).
from generate_primes import generate_prime
p_ = generate_prime()
q_ = generate_prime()

# Compute n = p·q — this is the modulus, part of both public and private key.
n = p_ * q_

# Compute Euler's totient φ(n) = (p-1)(q-1).
phi = (p_ - 1) * (q_ - 1)


# Choose public exponent e — almost always 65537 (small, has few 1-bits so exponentiation is fast, and it's coprime to φ(n)).
e = 65537


# Compute private exponent d = e⁻¹ mod φ(n) using the Extended Euclidean Algorithm.
# pow(e, -1, phi) is Python's built-in modular inverse (does the Extended Euclidean Algorithm under the hood) 
d = pow(e, -1, phi)

#  Public key = (n, e). Private key = (n, d) (plus p, q, and some precomputed values for speed — CRT optimization).
print("Public key:", (n, e))
print("Private key:", (n, d))

# --- Alice and Bob example ---
# Alice wants to send Bob the number 11228, and prove it really came from her.
# Alice signs it with HER private key. Bob verifies it with HER public key.

# NOTE: Message must be bigger than the n

message = 11228
if message < n:
    print("Message should be bigger than n (p * q)")
    exit()

# NOTE: Real RSA signs hash of the message not raw message
# message = sha256(message)

# Alice signs: signature = message^d mod n
signature = pow(message, d, n)
print("Alice sends message:", message)
print("Alice sends signature:", signature)

# Bob verifies: recovered = signature^e mod n
recovered = pow(signature, e, n)
print("Bob recovers:", recovered)

if recovered == message:
    print("Valid signature — this really came from Alice!")
else:
    print("Invalid signature — reject this message!")