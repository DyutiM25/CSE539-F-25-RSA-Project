#!/usr/bin/env python3
import sys
from math import gcd

# ----- Extended Euclidean Algorithm -----
def egcd(a, b):
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y
    return old_r, old_x, old_y

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("e and phi(n) are not coprime; inverse does not exist")
    return x % m

def generate_private_key(e, p, q):
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        raise ValueError("Public exponent e is not coprime with phi(n)")
    d = modinv(e, phi)
    return d

def decrypt(ciphertext, key, N):
    return pow(ciphertext, key, N)

def encrypt(plaintext, key, N):
    return pow(plaintext, key, N)

def main():
    if len(sys.argv) != 9:
        print("Usage: python3 rsa.py pe pc qe qc ee ec ciphertext plaintext")
        sys.exit(1)

    pe  = int(sys.argv[1]); pc  = int(sys.argv[2])
    qe  = int(sys.argv[3]); qc  = int(sys.argv[4])
    ee  = int(sys.argv[5]); ec  = int(sys.argv[6])
    C   = int(sys.argv[7])
    P   = int(sys.argv[8])

    # 1) Reconstruct big integers
    p = (1 << pe) - pc  # 2**pe - pc
    q = (1 << qe) - qc  # 2**qe - qc
    e = (1 << ee) - ec  # 2**ee - ec

    # 2) Compute n and private exponent d
    n = p * q
    d = generate_private_key(e, p, q)

    # 3) Decrypt and Encrypt
    decrypted = decrypt(C, d, n)
    encrypted = encrypt(P, e, n)

    # 4) Output exactly as required
    print(f"{decrypted}, {encrypted}")

if __name__ == "__main__":
    main()
