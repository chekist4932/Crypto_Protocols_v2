import random
import math

import json
import datetime


class RSA:
    def __init__(self):
        self.data = str(datetime.datetime.now())[:-7].replace(":", "-")
        pass

    def key_gen(self, key_digit):
        sec_key = [self.__PrimeNum(key_digit // 2, 100), self.__PrimeNum(key_digit // 2, 100)]  # [p, q, d]
        public_key = [sec_key[0] * sec_key[1]]  # [n = p*q, exp]
        phi = (sec_key[0] - 1) * (sec_key[1] - 1)
        while True:
            exp = random.randint(1, phi - 1)
            mod, a, d = self.__EucAlg(phi, exp)
            if mod ^ 1 == 0:
                if ((d * exp) % phi) ^ 1 == 0:
                    if d < 0:
                        d += phi
                    public_key.append(exp)
                    sec_key.append(d)
                    break
        return sec_key, public_key

    @staticmethod
    def encrypt(pub_key: list[int, int, int], bytes_mess: bytes):
        _N = pub_key[0] * pub_key[1]
        _exp = pub_key[2]
        _msg_len_bytes = len(bytes_mess)
        _key_byte_len = len((_N).to_bytes(math.ceil(math.log2((_N)) / 8), byteorder="big"))

        if _key_byte_len > 2048:
            _key_byte_len = 2048

        _block_len = _key_byte_len - 2
        _pad_bytes_size = math.ceil(math.log(_key_byte_len, 2) / 8)  # Нахожу размерность байтов для паддинга.
        # Округление в большую сторону кратность степени размера блока 8-ке
        # _pad_bytes_size = кратности степени размера блока 8-ке.

        _msg_blocks = [bytes_mess[x:x + _block_len] for x in range(0, _msg_len_bytes, _block_len)]

        for _block_in_msg in range(len(_msg_blocks)):
            _count_pad = (_block_len + 1) - len(_msg_blocks[_block_in_msg])
            _padding_byte = _count_pad.to_bytes(_pad_bytes_size, byteorder="big")

            for i in range(_count_pad):
                _msg_blocks[_block_in_msg] += _padding_byte

        _encrypted_msg_blocks = [pow(int.from_bytes(_block, byteorder='big'), _exp, (_N)) for
                                 _block in
                                 _msg_blocks.copy()]

        return b"".join([x.to_bytes(math.ceil(math.log2(x) / 8), byteorder="big") for x in _encrypted_msg_blocks])

    @staticmethod
    def decrypt(key: list[int, int], encrypted_msg: bytes):

        _msg_len_bytes = len(encrypted_msg)
        _key_byte_len = len(
            (key[0]).to_bytes(math.ceil(math.log2((key[0])) / 8), byteorder="big"))

        if _key_byte_len > 2048:
            _key_byte_len = 2048

        _block_len = _key_byte_len - 1

        _encrypted_msg_blocks = [int.from_bytes(encrypted_msg[x:x + _key_byte_len], "big") for x in
                                 range(0, _msg_len_bytes, _key_byte_len)]

        _decrypted_msg = [x.to_bytes(_block_len, byteorder="big") for x in
                          [pow(num, key[1], key[0]) for num in _encrypted_msg_blocks]]

        for _block_in_decrypted in range(len(_decrypted_msg)):
            _byte_check = _decrypted_msg[_block_in_decrypted][-1]
            __checker = 0
            for i in range(len(_decrypted_msg[_block_in_decrypted]) - 1, (_block_len - _byte_check) - 1, -1):
                if _decrypted_msg[_block_in_decrypted][i] == _byte_check:
                    __checker += 1

            if __checker == _byte_check:
                _decrypted_msg[_block_in_decrypted] = _decrypted_msg[_block_in_decrypted][:_block_len - __checker]
            else:
                raise ValueError("Wrong key")
        return b"".join(_decrypted_msg)

    def pkcs_8_12(self, secret_key: list[int], public_key: list[int], date):

        pub_k = {"SubjectPublicKeyInfo": {"publicExponent": public_key[1], "N": public_key[0]},
                 "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"}

        q_rev = self.__EucAlg(secret_key[0], secret_key[1])[2]

        sec_k = {'privateExponent': secret_key[2], 'prime1': secret_key[0], 'prime2': secret_key[1],
                 'exponent1': secret_key[2] % (secret_key[0] - 1),
                 'exponent2': secret_key[2] % (secret_key[1] - 1),
                 'coefficient': q_rev}

        file = open(f"results\\PubKey - {date}.json", "w")
        json.dump(pub_k, file, indent=4)
        file.close()

        file = open(f"results\\SecKey - {date}.json", "w")
        json.dump(sec_k, file, indent=4)
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
                    res = json.load(j_file)
                    result = [res["SubjectPublicKeyInfo"]["N"], res["SubjectPublicKeyInfo"]["publicExponent"]]
            elif mode == "sc":
                with open(path, "r", encoding="utf-8") as j_file:
                    res = json.load(j_file)
                    result = [res["prime1"], res["prime2"], res["privateExponent"]]
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

    @staticmethod
    def __EucAlg(x: int, y: int):
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
