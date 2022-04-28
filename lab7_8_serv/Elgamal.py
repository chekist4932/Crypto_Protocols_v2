import itertools
import random
import math

import json
import datetime
from sympy.ntheory import factorint, primerange
from math import gcd


class elgamal:
    def __init__(self):
        self.data = str(datetime.datetime.now())[:-7].replace(":", "-")
        pass

    def key_gen(self, key_digit):
        p = self.PrimeNum(key_digit, 100)
        a = random.randint(2, p - 2)
        alpha = self.gen_parent_element(p)
        public_key = {"SubjectPublicKeyInfo": {"alpha": alpha, "beta": pow(alpha, a, p), "p": p},
                      "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"}
        secret_key = {"privateExponent": a}
        """phi = (sec_key[0] - 1) * (sec_key[1] - 1)
        while True:
            exp = random.randint(1, phi - 1)
            mod, a, d = self.EucAlg(phi, exp)
            if mod ^ 1 == 0:
                if ((d * exp) % phi) ^ 1 == 0:
                    if d < 0:
                        d += phi
                    public_key.append(exp)
                    sec_key.append(d)
                    break"""
        return secret_key, public_key

    # @staticmethod
    def signature(self, public_key: dict, secret_key: dict, bytes_hash_mess: bytes):
        p = public_key["p"]
        while True:
            r = random.randint(1, p - 2)
            if gcd(r, p - 1) ^ 1 == 0:
                gamma = pow(public_key["alpha"], r, p)
                sigma = ((int.from_bytes(bytes_hash_mess, "big") - secret_key["privateExponent"] * gamma) * self.EucAlg(
                    p - 1, r)[2]) % (p - 1)

                return {"gamma": gamma, "sigma": sigma}

    @staticmethod
    def check_signature(public_key: dict, signature: dict, hash_: str):
        gamma = signature["gamma"]
        sigma = signature["sigma"]
        beta = public_key["beta"]
        alpha = public_key["alpha"]
        mod_p = public_key["p"]
        one = pow(beta, gamma, mod_p)
        two = pow(gamma, sigma, mod_p)
        third = pow(alpha, int.from_bytes(bytes.fromhex(hash_), "big"), mod_p)
        if (one*two)%mod_p == third:
            return True
        else:
            return False


    def pkcs_8_12(self, secret_key: dict, public_key: dict, date):

        file = open(f"results\\PubKey - {date}.json", "w")
        json.dump(public_key, file, indent=4)
        file.close()

        file = open(f"results\\SecKey - {date}.json", "w")
        json.dump(secret_key, file, indent=4)
        file.close()


    @staticmethod
    def read_out_file(path: str, mode: str):
        try:
            if mode == "msg":
                with open(path, "r", encoding="utf-8") as file:
                    result = file.read()
            elif mode == "en_msg":
                with open(path, "r", encoding="utf-8") as j_file:
                    result = json.load(j_file)['EncryptedContentInfo']["encryptedContent"]
            elif mode == "pb":
                with open(path, "r", encoding="utf-8") as j_file:
                    result = json.load(j_file)["SubjectPublicKeyInfo"]
            elif mode == "sc":
                with open(path, "r", encoding="utf-8") as j_file:
                    result = json.load(j_file)
            else:
                raise ValueError("Uncorrect mode")
        except Exception as err:
            raise err
        else:
            return result

    @staticmethod
    def __test_miller(flag: list):
        # BODY
        n = flag[0]
        a = flag[1]
        exp = n - 1

        while not exp & 1:
            exp >>= 1

        if pow(a, exp, n) == 1:
            return True

        while exp < n - 1:
            if pow(a, exp, n) == n - 1:
                return True

            exp <<= 1

        return False

    def PrimeNum(self, prime_size, iter_count):
        def check(maybe_prime):
            for step in range(iter_count):
                if self.__test_miller([maybe_prime, random.randint(2, maybe_prime - 2)]) is True:
                    if step == iter_count - 1:
                        return maybe_prime
                    else:
                        continue
                else:
                    return False

        while True:
            prime = []
            for i in range(prime_size):
                prime.append(str(round(random.random())))
            prime[0] = "1"
            prime[-1] = "1"
            p = int("".join(prime), 2)
            if check(p) is False:
                continue
            else:
                break
        return p

    @staticmethod
    def EucAlg(x: int, y: int):
        if x >= y:
            pass
        elif x < y:
            mp = x
            x = y
            y = mp
        # BODY
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


    def gen_parent_element(self, prime_mod):
        for maybe_parent in primerange(2, prime_mod):
            flag = True
            if gcd(prime_mod, maybe_parent) ^ 1 == 0 and pow(maybe_parent, (prime_mod - 1) // 2, prime_mod) ^ 1 != 0:
                for prime in list(factorint(prime_mod - 1).keys()):
                    if pow(maybe_parent, (prime_mod - 1) // prime, prime_mod) ^ 1 == 0:
                        flag = False
                        break
                if flag:
                    return maybe_parent
