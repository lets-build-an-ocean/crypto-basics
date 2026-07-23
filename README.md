# Hello to everyone reading in English! 👋

In this repo I want to walk step by step through one of the most important and newest **post-quantum digital signature** algorithms — one designed to resist attacks from quantum computers.

If, like me, you don't have patience for long papers, you're in the right place. This takes less than **10 minutes** to read, but by the end you'll have a solid picture of what a digital signature is and why post-quantum signatures matter.

---

# What is a digital signature?

A digital signature is something attached to a message or file so anyone can check:

- Did this message really come from the sender?
- Has the message changed since it was sent?

That's exactly what digital signatures are designed to answer.

> **Note:** A digital signature does not hide or encrypt the message. Anyone can see the message's content — the signature only confirms who sent it and that it wasn't tampered with.

## An example

Suppose Alice wants to send a PDF file to Bob.

Before sending, Alice uses her **private key** to create a **digital signature** for the file. Then she sends Bob two things:

- The PDF file
- The file's digital signature

Bob uses Alice's **public key** to check the signature against the file he received.

If the signature checks out, Bob can be confident that:

- The file was signed by whoever holds the private key (Alice).
- The file hasn't changed since it was signed.

If even one letter, digit, or bit of the file changes, the signature check fails and Bob knows the file isn't trustworthy.

---

## RSA in simple terms

RSA is the oldest and most widely used digital signature scheme. Here's the easy way to picture it:

- You make a public padlock anyone can snap shut (your **public key**), but only you hold the key that opens it (your **private key**).
- To sign, instead of locking the whole message, you take a short fingerprint (a hash) of it and "lock" that fingerprint with your private key. Anyone can unlock it with your public key and check the fingerprint matches the message.

**Where does RSA's security come from?**
You multiply two huge, secret prime numbers together to get a number `n`. Multiplying them is easy. But if all someone has is `n`, working backward to find those two primes (factoring `n`) is brutally hard for classical computers.

**So what's the problem?**
Shor's algorithm, run on a quantum computer, can factor `n` quickly. Once quantum computers are powerful enough, RSA stops being safe — that's the whole motivation for schemes like ML-DSA.

## ML-DSA in simple terms (post-quantum)

Instead of relying on "factoring big numbers," ML-DSA relies on a geometric problem called the **lattice problem** — one that, as far as we know, quantum computers have no fast trick for either.

Here's the easy way to picture it:

- There's a public grid, or "matrix" (`A`), that everyone can see — think of it as a big, public maze.
- Your private key is a short, simple secret path through that maze (a vector `s1`).
- Your public key (`t`) is just where that path ends up: `t = A·s1`. Given only the endpoint, finding the secret path that leads there is essentially impossible — even for a quantum computer.
- To sign, you take a fresh random hop (`y`), see where it lands (`w = A·y`), then build a small "challenge" number (`c`) from the message and `w`, and mix it into your secret path: `z = y + c·s1`.
- You only ever send `(z, c)` — never the secret path or the random hop. The recipient can rebuild `w` from your public key and these two numbers alone, check it produces the same challenge `c`, and thus verify the signature.

## Why does this matter?

Both schemes share the same core idea: a **hard problem** that's easy to verify but brutally hard to reverse. The difference is that RSA's hard problem (factoring) falls to quantum computers, while lattice problems so far appear resistant — which is why researchers are building and studying post-quantum schemes like ML-DSA.

## The code

- `rsa.py` — a minimal RSA implementation
- `ml_dsa.py` — a simplified ML-DSA implementation (for easier learning; it skips the error term and high-bit rounding that real ML-DSA uses)

*(نسخه‌ی فارسی: [README.md](README.md))*
