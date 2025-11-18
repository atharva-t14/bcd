#!/usr/bin/env python3
"""
Exp04 - Diffie-Hellman Key Exchange
Author: Atharva Tamhankar
UID: 2022300127
Experiment: Exp04
"""

import secrets
import hashlib
import sys

DEFAULT_G = 2

# ---------- Miller-Rabin primality test ----------
def is_probable_prime(n, k=8):
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=512):
    while True:
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(candidate):
            return candidate

# ---------- Key Derivation ----------
def kdf_sha256(shared_int):
    length = (shared_int.bit_length() + 7) // 8
    s_bytes = shared_int.to_bytes(length if length > 0 else 1, "big")
    return hashlib.sha256(s_bytes).digest()

# ---------- Demo XOR cipher (not secure) ----------
def xor_stream(data: bytes, key: bytes) -> bytes:
    out = bytearray()
    for i, b in enumerate(data):
        out.append(b ^ key[i % len(key)])
    return bytes(out)

# ---------- Menu ----------
def menu():
    state = {
        "p": None, "g": None,
        "alice": None, "bob": None,
        "shared_alice": None, "shared_bob": None,
        "derived_key": None
    }

    def pick_params():
        print("\n1) Generate demo prime (512/1024 bits)")
        print("2) Enter custom p and g")
        choice = input("Choose option: ").strip()
        if choice == "1":
            bits = input("Bit-length (default 512): ").strip()
            bits = int(bits) if bits.isdigit() else 512
            p = generate_prime(bits)
            g = DEFAULT_G
        elif choice == "2":
            p = int(input("Enter p (prime): "))
            g = int(input("Enter g (generator): "))
        else:
            print("Invalid option.")
            return
        state["p"], state["g"] = p, g
        print(f"Selected p (bits={p.bit_length()}), g={g}")

    def gen_keys():
        if state["p"] is None:
            print("Select parameters first.")
            return
        hide = input("Hide private keys? (y/n) [y]: ").strip().lower() or "y"
        hide_bool = hide == "y"
        a = secrets.randbelow(state["p"] - 3) + 2
        b = secrets.randbelow(state["p"] - 3) + 2
        A = pow(state["g"], a, state["p"])
        B = pow(state["g"], b, state["p"])
        state["alice"] = {"priv": a if not hide_bool else None, "priv_val": a, "pub": A}
        state["bob"] = {"priv": b if not hide_bool else None, "priv_val": b, "pub": B}
        print("Generated keys.")
        print("Alice pub A =", A)
        print("Bob   pub B =", B)
        if not hide_bool:
            print("Alice priv a =", a)
            print("Bob   priv b =", b)

    def compute_shared_secret():
        if not state["alice"] or not state["bob"]:
            print("Generate keys first.")
            return
        a = state["alice"]["priv_val"]
        b = state["bob"]["priv_val"]
        A = state["alice"]["pub"]
        B = state["bob"]["pub"]
        K_a = pow(B, a, state["p"])
        K_b = pow(A, b, state["p"])
        state["shared_alice"], state["shared_bob"] = K_a, K_b
        print("Shared secret computed.")
        print("K_A bits =", K_a.bit_length())
        print("K_B bits =", K_b.bit_length())
        print("Equal?:", "Yes" if K_a == K_b else "No")

    def derive_and_demo():
        if state["shared_alice"] is None:
            print("Compute shared secret first.")
            return
        K = state["shared_alice"]
        key = kdf_sha256(K)
        state["derived_key"] = key
        print("Derived key (SHA-256):", key.hex())
        msg = input("Enter plaintext: ").encode()
        cipher = xor_stream(msg, key)
        plain = xor_stream(cipher, key)
        print("Ciphertext (hex):", cipher.hex())
        print("Recovered:", plain.decode(errors="replace"))

    def show_state():
        print("\nState summary:")
        print("p bits:", state["p"].bit_length() if state["p"] else None)
        print("g:", state["g"])
        print("Alice pub:", state["alice"]["pub"] if state["alice"] else None)
        print("Bob   pub:", state["bob"]["pub"] if state["bob"] else None)
        print("Shared equal?:",
              (state["shared_alice"] == state["shared_bob"]) if state["shared_alice"] else None)

    actions = {
        "1": pick_params,
        "2": gen_keys,
        "3": compute_shared_secret,
        "4": derive_and_demo,
        "5": show_state,
        "q": lambda: sys.exit(0),
    }

    while True:
        print("\n=== Diffie-Hellman Lab Menu ===")
        print("1) Select / Generate Public Parameters (p, g)")
        print("2) Generate Keys for Alice and Bob")
        print("3) Compute Shared Secret")
        print("4) Derive Key & Encrypt/Decrypt (demo)")
        print("5) Show State")
        print("q) Quit")
        choice = input("Choice: ").strip()
        if choice in actions:
            try:
                actions[choice]()
            except Exception as e:
                print("Error:", e)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    print("Diffie-Hellman Lab Demo — Exp04")
    # print("Author: Atharva Tamhankar (UID: 2022300127)")
    menu()
