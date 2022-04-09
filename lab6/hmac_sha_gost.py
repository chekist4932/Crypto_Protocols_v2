# Лабораторная работа №6
# Реализация хеш-функции HMAC

import random
import math
from GOST_R_34_12_2012 import GOST_34_11_2012
from sha_256_512 import sha_256, sha_512


class hmac_hash:

    def XOR_(self, vec_1: bytes, vec_2: bytes) -> bytes:
        int_enc = int.from_bytes(vec_2, "big") ^ int.from_bytes(vec_1, "big")
        return int_enc.to_bytes(max(len(vec_1), len(vec_2)), "big")

    def generation_key(self) -> bytes:
        key_size = random.randint(256, 1024)
        key = self.__PrimeNum(key_size, 50)
        _key = key.to_bytes(math.ceil(key_size / 8), byteorder="big")
        return _key

    #  H( (K_⊕Opad) || H( (K_⊕Ipad) || M ) )
    def sha_(self, bytes_message: bytes, key_: bytes, size: int) -> bytes:
        if size == 256:

            _b_block = 64
            key_0 = key_

            if len(key_) > _b_block:
                key_0 = sha_256(key_)
                key_0 += b"\x00" * (_b_block - len(key_0))

            elif len(key_) < _b_block:
                key_0 += b"\x00" * (_b_block - len(key_0))

        elif size == 512:

            _b_block = 128
            key_0 = key_

            if len(key_) > _b_block:
                key_0 = sha_512(key_)
                key_0 += b"\x00" * (_b_block - len(key_0))

            elif len(key_) < _b_block:
                key_0 += b"\x00" * (_b_block - len(key_0))
        else:
            raise ValueError("Size got 256 or 512")


        _Ipad = b"\x36" * _b_block
        _Opad = b"\x5c" * _b_block

        if size == 256:
            First_hash = sha_256(self.XOR_(key_0, _Ipad) + bytes_message)
            _hash = sha_256(self.XOR_(key_0, _Opad) + First_hash)
        elif size == 512:
            First_hash = sha_512(self.XOR_(key_0, _Ipad) + bytes_message)
            _hash = sha_512(self.XOR_(key_0, _Opad) + First_hash)

        return _hash

    def gost_stribog(self, bytes_message: bytes, key_: bytes, size: int) -> bytes:
        if size == 256:

            _b_block = 64
            key_0 = key_

            if len(key_) > _b_block:

                key_0 = GOST_34_11_2012(key_, 256).hash_()
                key_0 += b"\x00" * (_b_block - len(key_0))

            elif len(key_) < _b_block:
                key_0 += b"\x00" * (_b_block - len(key_0))

        elif size == 512:

            _b_block = 64
            key_0 = key_

            if len(key_) > _b_block:

                key_0 = GOST_34_11_2012(key_, 512).hash_()
                key_0 += b"\x00" * (_b_block - len(key_0))

            elif len(key_) < _b_block:
                key_0 += b"\x00" * (_b_block - len(key_0))

        else:
            raise ValueError("Size got 256 or 512")


        _Ipad = b"\x36" * _b_block
        _Opad = b"\x5c" * _b_block

        if size == 256:
            First_hash = GOST_34_11_2012(self.XOR_(key_0, _Ipad) + bytes_message, 256).hash_()
            _hash = GOST_34_11_2012(self.XOR_(key_0, _Opad) + First_hash, 256).hash_()
        elif size == 512:
            First_hash = GOST_34_11_2012(self.XOR_(key_0, _Ipad) + bytes_message, 512).hash_()
            _hash = GOST_34_11_2012(self.XOR_(key_0, _Opad) + First_hash, 512).hash_()

        return _hash

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

    def __PrimeNum(self, prime_size, iter_count):
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
