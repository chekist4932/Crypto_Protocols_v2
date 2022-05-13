import itertools
import json
import random
import time
import timeit
import math
import sympy


class RsaKeys:

    def under_group_params(self, key_digit):
        prime_1 = self.prime_num(key_digit)
        prime_2 = self.prime_num(key_digit)
        phi = (prime_1 - 1) * (prime_2 - 1)
        while True:
            exp = random.randint(1, phi - 1)
            mod, a, d = self.alg_euc(phi, exp)
            if mod ^ 1 == 0 and ((d * exp) % phi) ^ 1 == 0:
                if d < 0:
                    d += phi

                break
        return prime_1 * prime_2, exp, d

    def gen_parent_element(self, prime_mod):
        for maybe_parent in range(2, prime_mod):
            if pow(maybe_parent, 2, prime_mod) ^ 1 != 0 and pow(maybe_parent, (prime_mod - 1) // 2, prime_mod) ^ 1 != 0:
                log_parent = int(math.log(prime_mod, maybe_parent))
                while True:
                    random_power = random.randint(log_parent // 2, log_parent)
                    if math.gcd(random_power, prime_mod - 1) ^ 1 == 0:
                        break
                new_parent = maybe_parent ** random_power
                return new_parent

    def prime_num(self, prime_size):
        while True:
            prime = [str(round(random.random())) for _ in range(prime_size)]
            prime[0] = "1"
            prime[-1] = "1"
            p = int("".join(prime), 2)
            if sympy.isprime(p) is False:
                continue
            else:
                break
        return p

    @staticmethod
    def alg_euc(x: int, y: int):
        if x < y:
            mp = x
            x = y
            y = mp
        A = [0, 1]
        B = [1, 0]
        nod, a, b = 0, 0, 0
        while y != 0:
            q = x // y
            r = x - q * y
            a = A[1] - q * A[0]
            b = B[1] - q * B[0]
            x = y
            y = r
            A[1] = A[0]
            A[0] = a
            B[1] = B[0]
            B[0] = b
            nod = x
            a = A[1]
            b = B[1]
        return nod, a, b

# num = 31413525216
# str_num = json.dumps(num)
# bytes_num = str_num.encode()
# print(bytes_num)
# print(json.loads(bytes_num.decode()) == num)