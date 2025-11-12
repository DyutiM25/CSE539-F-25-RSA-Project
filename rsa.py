import sys
from math import gcd

# Extended Euclidean Algorithm to find modular inverse
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

# Modular Inverse
def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("e and phi(n) are not coprime; inverse does not exist")
    return x % m

# Generate private key d from public exponent e and primes p, q
def generate_private_key(e, p, q):
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        raise ValueError("Public exponent e is not coprime with phi(n)")
    d = modinv(e, phi)
    return d

# RSA Encrypt and Decrypt functions
def encrypt(plaintext, key, N):
    return pow(plaintext, key, N)
def decrypt(ciphertext, key, N):
    return pow(ciphertext, key, N)

# Main function
def main():
    if len(sys.argv) != 9:
        print("Usage: python3 rsa.py pe pc qe qc ee ec ciphertext plaintext")
        sys.exit(1)

    pe  = int(sys.argv[1]); pc  = int(sys.argv[2])
    qe  = int(sys.argv[3]); qc  = int(sys.argv[4])
    ee  = int(sys.argv[5]); ec  = int(sys.argv[6])
    C   = int(sys.argv[7])
    P   = int(sys.argv[8])

    # 1. Compute p = 2**pe - pc, q = 2**qe - qc, e = 2**ee - ec
    p = (1 << pe) - pc  
    q = (1 << qe) - qc  
    e = (1 << ee) - ec  

    # 2. Compute n = p * q and d = private key
    n = p * q
    d = generate_private_key(e, p, q)

    # 3. Decrypt ciphertext and Encrypt plaintext
    decrypted = decrypt(C, d, n)
    encrypted = encrypt(P, e, n)

    # 4. Print results
    print(f"{decrypted}, {encrypted}")

if __name__ == "__main__":
    main()
