"""Toy Learning With Errors (LWE) Post-Quantum Public-Key Encryption."""

import random


class ToyLWE:
    def __init__(self, n: int = 4, q: int = 97):
        self.n = n          # Dimension of secret vector
        self.q = q          # Prime modulus
        # Private key: small secret vector s
        self.secret_s = [random.randint(0, 1) for _ in range(n)]

    def generate_public_sample(self) -> tuple[list[int], int]:
        """Generates sample (a, b) where b = a*s + error (mod q)."""
        a = [random.randint(0, self.q - 1) for _ in range(self.n)]
        small_error = random.choice([-1, 0, 1])
        inner_prod = sum(ai * si for ai, si in zip(a, self.secret_s))
        b = (inner_prod + small_error) % self.q
        return a, b

    def encrypt_bit(self, bit: int, pub_samples: list[tuple[list[int], int]]) -> tuple[list[int], int]:
        """Encrypts a single bit (0 or 1) using a subset sum of public samples."""
        subset_indices = [i for i in range(len(pub_samples)) if random.random() < 0.5]
        if not subset_indices:
            subset_indices = [0]

        u = [0] * self.n
        v = 0
        for idx in subset_indices:
            a, b = pub_samples[idx]
            for i in range(self.n):
                u[i] = (u[i] + a[i]) % self.q
            v = (v + b) % self.q

        # Add message payload: 0 encodes to 0, 1 encodes to round(q / 2)
        message_shift = (self.q // 2) if bit == 1 else 0
        v = (v + message_shift) % self.q
        return u, v

    def decrypt(self, u: list[int], v: int) -> int:
        """Decrypts ciphertext (u, v) using secret key s."""
        inner_prod = sum(ui * si for ui, si in zip(u, self.secret_s))
        dec = (v - inner_prod) % self.q

        # Distance to 0 vs distance to q/2
        half_q = self.q / 2
        dist_to_0 = min(dec, self.q - dec)
        dist_to_half = abs(dec - half_q)

        return 1 if dist_to_half < dist_to_0 else 0


if __name__ == "__main__":
    lwe = ToyLWE(n=4, q=97)
    public_key = [lwe.generate_public_sample() for _ in range(12)]

    print(f"Secret Key (s): {lwe.secret_s}")
    print(f"Modulus (q): {lwe.q}")

    # Test bit encryption & decryption
    test_bits = [1, 0, 1, 1, 0]
    decrypted_bits = []

    for bit in test_bits:
        ciphertext = lwe.encrypt_bit(bit, public_key)
        recovered = lwe.decrypt(*ciphertext)
        decrypted_bits.append(recovered)

    print(f"Original Bits:  {test_bits}")
    print(f"Decrypted Bits: {decrypted_bits}")
    print("Match:", test_bits == decrypted_bits)
