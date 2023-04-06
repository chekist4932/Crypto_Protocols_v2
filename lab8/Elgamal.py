import itertools
import random
import math

import json
import datetime
import timeit

from sympy.ntheory import factorint, primerange, isprime
from math import gcd
import pyprimes


class elgamal:
    def __init__(self):
        self.data = str(datetime.datetime.now())[:-7].replace(":", "-")
        pass

    def key_gen(self, key_digit):
        p = self.PrimeNum(key_digit, 100)
        a = random.randint(2, p - 2)
        alpha = self.gen_parent_element(p)
        public_key = {"alpha": alpha, "beta": pow(alpha, a, p), "p": p}
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
        hash_int = int.from_bytes(bytes_hash_mess, "big")
        while True:
            r = random.randint(1, p - 2)
            if gcd(r, p - 1) ^ 1 == 0:
                gamma = pow(public_key["alpha"], r, p)
                sigma = (hash_int - (secret_key["privateExponent"] * gamma))  # % (p - 1)
                sigma = pow(sigma * self.EucAlg(p - 1, r)[2], 1, p - 1)

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
        if (one * two) % mod_p == third:
            return True
        else:
            return False

    def pkcs_8_12(self, secret_key: dict, public_key: dict, date):
        pub_key = {
            "SubjectPublicKeyInfo": {"alpha": public_key["alpha"], "beta": public_key["beta"], "p": public_key["p"]},
            "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"}
        file = open(f"results\\PubKey - {date}.json", "w")
        json.dump(pub_key, file, indent=4)
        file.close()

        file = open(f"results\\SecKey - {date}.json", "w")
        json.dump(secret_key, file, indent=4)
        file.close()

    @staticmethod
    def PKCS_7_CAdES(msg, signature, hash_type, public_key, mark):
        signature_ = {"CMSVersion": "1", "DigestAlgorithmIdentifiers": hash_type,
                      "EncapsulatedContentInfo": {"ContentType": "text", "OCTET STRING": msg},
                      "CertificateSet": {
                          "SubjectPublicKeyInfo": {"alpha": public_key["alpha"], "beta": public_key["beta"],
                                                   "p": public_key["p"]},
                          "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"},
                      "RevocationInfoChoises": "NULL",
                      "SignerInfos":
                          {"CMSVersion": "1", "SignerIdentifier": "Цой Георгий",
                           "DigestAlgorithmIdentifier": hash_type,
                           "SignedAttributes": "NULL",
                           "SignatureAlgorithmIdentifier": "ELGAMALdsi",
                           "SignatureValue": signature,
                           "UnsignedAttributes":
                               {"OBJECT IDENTIFIER": "signature-time-stamp",
                                "SET OF AttributeValue":
                                    " "
                                }
                           }
                      }
        file = open(f"results\\Signature {mark}.json", "w", encoding="utf-8")
        json.dump(signature_, file, indent=4)
        file.close()
        return signature_

    @staticmethod
    def read_out_file(path: str, mode: str):
        try:
            if mode == "msg":
                with open(path, "r", encoding="utf-8") as file:
                    result = file.read().encode("utf-8")
            elif mode == "en_msg":
                with open(path, "r", encoding="utf-8") as j_file:
                    result = json.load(j_file)['EncryptedContentInfo']["encryptedContent"]
            elif mode == "pb":
                with open(path, "r", encoding="utf-8") as j_file:
                    result = json.load(j_file)["SubjectPublicKeyInfo"]
            elif mode == "sk":
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

    def prime_del(self, numb):
        numb_list = []
        for div in range(numb - 1, 5, -1):
            if (numb % div == 0):
                if self.__test_miller([div, random.randint(2, div - 2)]) is True:
                    numb_list.append(div)
        if numb % 5 == 0:
            numb_list.append(5)
        if numb % 3 == 0:
            numb_list.append(3)
        if numb % 2 == 0:
            numb_list.append(2)
        return numb_list

    def gen_parent_element(self, prime_mod):
        for maybe_parent in range(2, prime_mod):
            flag = True
            if pow(maybe_parent, (prime_mod - 1) // 2, prime_mod) ^ 1 != 0:
                for prime in list(factorint(prime_mod - 1).keys()):
                # for prime in pyprimes.factorise(prime_mod - 1):
                    if pow(maybe_parent, (prime_mod - 1) // prime, prime_mod) ^ 1 == 0:
                        flag = False
                        break
                if flag:
                    log_parent = int(math.log(prime_mod, maybe_parent))
                    # print(f"log parent - {log_parent}")
                    print(maybe_parent)
                    while True:
                        random_power = random.randint(log_parent // 2, log_parent)
                        if gcd(random_power, prime_mod - 1) ^ 1 == 0:
                            break
                    # print(f"random pow - {random_power}")
                    new_parent = maybe_parent ** random_power
                    # print(f"new parent - {new_parent}")
                    return new_parent


# for i in range(1):
#     obj = elgamal()
#
#     # p = obj.PrimeNum(256, 100)o
#     prime = obj.PrimeNum(12, 100)
#     print(f"prime - {prime}")
#     parent = obj.gen_parent_element(prime)
#     print(f"parent - {parent}")
#     log_parent = int(math.log(prime, parent))
#     print(f"log parent - {log_parent}")
#     while True:
#         random_power = random.randint(log_parent//2, log_parent)
#         if gcd(random_power, prime-1) ^ 1 == 0:
#             break
#     print(f"random pow - {random_power}")
#     new_parent = parent**random_power
#     print(f"new parent - {new_parent}")
#     list_ex = [num for num in range(1, prime)]
#     list_check = []
#     for num in range(prime):
#         list_check.append(pow(new_parent,num,prime))
#     list_check = list(set(list_check))
#     list_check.sort()
#     # print(list_ex)
#     # print(list_check)
#     print("\t\t\t",list_ex == list_check)


obj = elgamal()
#
# prime = obj.PrimeNum(16, 100)
# print(f"Prime - {prime}")
# print(f"Is prime? - {isprime(prime)}")
# parent = obj.PrimeNum(8,100)
# print(f"Parent - {parent}")
# print(f"Is prime? - {isprime(parent)}")
# list_ex = [num for num in range(1, prime)]
# list_check = []
# for num in range(prime):
#     list_check.append(pow(parent,num,prime))
# list_check = list(set(list_check))
# list_check.sort()
# # print(list_ex)
# # print(list_check)
# print(f"Len is example - {len(list_ex)}")
# print(f"Len my result - {len(list_check)}")
# print("\t\t\t",list_ex == list_check)
# if not list_ex == list_check:
#
#     pass
p1 = obj.PrimeNum(256,100)
print(p1)
print(obj.gen_parent_element(p1))
# print(prime)
# # print(timeit.timeit(lambda : factorint(prime-1), number= 1))
# print(timeit.timeit(lambda: pyprimes.factorise(prime - 1), number=1))
# for division in pyprimes.factorise(prime - 1):
#     print(division[0])
# print(f"RESULT CHECK  - {obj.gen_parent_element(prime)}")
print(pow(6, 87058861811474967159212354848651099066670359079678693517184707706407782575811-1, 87058861811474967159212354848651099066670359079678693517184707706407782575811))