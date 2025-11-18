import random
from math import gcd

# ---------- Modular arithmetic helpers ----------
def mod_exp(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result

def mod_inverse(e, phi):
    # Extended Euclidean Algorithm
    t, newt = 0, 1
    r, newr = phi, e
    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
    if r > 1:
        return None
    if t < 0:
        t += phi
    return t

# ---------- Prime generation ----------
def is_prime(n, k=5):
    if n < 2: return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
        if n % p == 0:
            return n == p
    # Miller-Rabin
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True

def generate_prime(bits=8):
    while True:
        candidate = random.getrandbits(bits)
        candidate |= 1
        if is_prime(candidate):
            return candidate

# ---------- RSA Implementation ----------
class RSA:
    def __init__(self, bits=8):
        self.p = generate_prime(bits)
        self.q = generate_prime(bits)
        while self.q == self.p:
            self.q = generate_prime(bits)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

        self.e = 3
        while gcd(self.e, self.phi) != 1:
            self.e += 2

        self.d = mod_inverse(self.e, self.phi)

    def encrypt(self, m):
        return mod_exp(m, self.e, self.n)

    def decrypt(self, c):
        return mod_exp(c, self.d, self.n)

# ---------- Menu ----------
def main():
    rsa = None
    while True:
        print("\n--- RSA MENU ---")
        print("1. Generate RSA Keys")
        print("2. Encrypt Message")
        print("3. Decrypt Message")
        print("4. Quit")

        choice = input("Enter choice: ")

        if choice == "1":
            rsa = RSA(bits=8)
            print(f"Primes p={rsa.p}, q={rsa.q}")
            print(f"Public Key (e, n): ({rsa.e}, {rsa.n})")
            print(f"Private Key (d, n): ({rsa.d}, {rsa.n})")

        elif choice == "2":
            if rsa is None:
                print("Generate keys first!")
                continue
            m = int(input("Enter message (number < n): "))
            c = rsa.encrypt(m)
            print(f"Ciphertext: {c}")

        elif choice == "3":
            if rsa is None:
                print("Generate keys first!")
                continue
            c = int(input("Enter ciphertext: "))
            m = rsa.decrypt(c)
            print(f"Decrypted Message: {m}")

        elif choice == "4":
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
