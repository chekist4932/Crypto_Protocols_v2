import itertools
import random
import math

import json
import datetime
import timeit

from sympy.ntheory import factorint, primerange, isprime
from math import gcd
import pyprimes

import GOST_R_34_12_2012
import sha_256_512


class Shamir:
    def __init__(self):
        self.data = str(datetime.datetime.now())[:-7].replace(":", "-")
        pass

    def key_gen(self, key_digit, size_):
        _p = self.PrimeNum(key_digit, 100)
        _q = self.PrimeNum(key_digit, 100)
        _n = _p * _q
        _a_values = tuple(random.randint(1, _n - 1) for step in range(size_))
        _b_values = tuple(pow(self.EucAlg(_n, a)[2], 2, _n) for a in _a_values)
        public_key = {"publicExponent": _b_values, "N": _n}
        secret_key = {'privateExponent': _a_values, 'prime1': _p, 'prime2': _q}
        return secret_key, public_key

    # @staticmethod
    def signature(self, secret_key: dict, bytes_mess: bytes, hash_type: str):

        a_values = secret_key['privateExponent']
        n = secret_key["prime1"] * secret_key["prime2"]
        r = random.randint(1, n - 1)
        u = pow(r, 2, n)
        to_hashing = bytes_mess + u.to_bytes(math.ceil(math.log2(u) / 8), "big")
        if hash_type[:-3] == "sha":
            hash_msg = sha_256_512.sha_(to_hashing, len(a_values))
            pass
        elif hash_type[:-3] == "GOST":
            hash_msg = GOST_R_34_12_2012.GOST_34_11_2012(to_hashing, len(a_values)).hash_()
        else:
            raise ValueError("Incorrect hash type")

        t = r
        for ind, byte_ in enumerate(hash_msg):
            for shift in range(8):
                t *= pow(a_values[ind * 8 + shift], (byte_ >> (7 - shift) & 1), n)
        t %= n

        return {"s": hash_msg.hex(), "t": t}

    @staticmethod
    def check_signature(public_key: dict, signature: dict, bytes_mess: bytes, hash_type: str):
        _b_values = public_key["publicExponent"]
        n = public_key["N"]
        hash_msg = bytes.fromhex(signature['s'])
        t = signature["t"]
        w = t ** 2
        for ind, byte_ in enumerate(hash_msg):
            for shift in range(8):
                w *= pow(_b_values[ind * 8 + shift], (byte_ >> (7 - shift) & 1), n)
        w %= n
        if hash_type[:-3] == "sha":
            hash_check = sha_256_512.sha_(bytes_mess + w.to_bytes(math.ceil(math.log2(w) / 8), "big"), len(_b_values))

        elif hash_type[:-3] == "GOST":
            hash_check = GOST_R_34_12_2012.GOST_34_11_2012(bytes_mess + w.to_bytes(math.ceil(math.log2(w) / 8), "big"),
                                                         len(_b_values)).hash_()
        else:
            raise ValueError("Incorrect hash type")
        if hash_check == hash_msg:
            return True
        else:
            return False

    def pkcs_8_12(self, secret_key: dict, public_key: dict, date):
        pub_key = {
            "SubjectPublicKeyInfo": {"publicExponent": public_key["publicExponent"], "N": public_key["N"]},
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
                          "SubjectPublicKeyInfo": {"publicExponent": public_key["publicExponent"], "N": public_key["N"]},
                          "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"},
                      "RevocationInfoChoises": "NULL",
                      "SignerInfos":
                          {"CMSVersion": "1", "SignerIdentifier": "Цой Георгий",
                           "DigestAlgorithmIdentifier": hash_type,
                           "SignedAttributes": "NULL",
                           "SignatureAlgorithmIdentifier": "FiatSHAMIRdsi",
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
            elif mode == "pb":
                with open(path, "r", encoding="utf-8") as j_file:
                    result = json.load(j_file)["SubjectPublicKeyInfo"]
            elif mode == "sk":
                with open(path, "r", encoding="utf-8") as j_file:
                    result = json.load(j_file)
            else:
                raise ValueError("Incorrect mode")
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



# p = obj.PrimeNum(256, 100)
# q = obj.PrimeNum(256, 100)
# n = p * q


# hash_type = "sha" + str(size_)
# a_values = [random.randint(1, n - 1) for step in range(size_)]
# b_values = [pow(obj.EucAlg(n, a)[2], 2, n) for a in a_values]
# for i in range(100):
#     a_values = [random.randint(2**128, 2**256) for step in range(size_)]
#     for j in a_values:
#         if a_values.count(j) != 1:
#             print("error")

# print(a_values)
# print(b_values)

# pub_key = {"SubjectPublicKeyInfo": {"publicExponent": b_values, "N": n},
#            "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"}
# sec_key = {'privateExponent': a_values, 'prime1': p, 'prime2': q}
#
# r = random.randint(1, n - 1)
# u = pow(r, 2, n)
# hash_msg = sha_256_512.sha_(msg + u.to_bytes(math.ceil(math.log2(u) / 8), "big"), size_)
# t = r
# for ind, byte_ in enumerate(hash_msg):
#     for shift in range(8):
#         t *= pow(a_values[ind * 8 + shift], (byte_ >> (7 - shift) & 1), n)
# t %= n
#
# w = t ** 2
#
# for ind, byte_ in enumerate(hash_msg):
#     for shift in range(8):
#         w *= pow(b_values[ind * 8 + shift], (byte_ >> (7 - shift) & 1), n)
# w %= n
# new_hash_msg = sha_256_512.sha_(msg + w.to_bytes(math.ceil(math.log2(w) / 8), "big"), size_)
#
# print(hash_msg == new_hash_msg)
# obj = Shamir()
# msg = "Hello guys".encode()
# size_ = 256
#
# sec, pub = obj.key_gen(512, 256)
# signature = obj.signature(sec, msg)
#
# print(obj.check_signature(pub, signature, msg))
