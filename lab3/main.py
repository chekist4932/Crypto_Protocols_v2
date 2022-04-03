import numpy as np
import timeit
import random
import math
import struct
import json
import datetime


class RSA:
    def __init__(self):
        # self.bin_mess = bin(int.from_bytes(mess_bytes, "big" ))[2:].zfill((len(mess_bytes.hex())//2)*8)
        pass

    def __hex_to_bin_v3(self, mess_bytes: bytes):
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

    def pkcs_7_8_12(self, encrypted_msg: list[int], secret_key: list[int], public_key: list[int]):
        # encr = [x.to_bytes(math.ceil(math.log2(x) / 8), byteorder="big").hex() for x in encrypted_msg]
        date = str(datetime.datetime.now())[:-7].replace(":", "-")
        res = {"Version": 0,
               "EncryptedContentInfo":
                   {"ContentType": "text",
                    "ContentEncryptionAlgorithmIdentifier": "rsaEncryption",
                    "encryptedContent": "".join(
                        [x.to_bytes(math.ceil(math.log2(x) / 8), byteorder="big").hex() for x in encrypted_msg]),
                    "OPTIONAL": "NULL"}}

        pub_k = {"SubjectPublicKeyInfo": {"publicExponent": public_key[1], "N": public_key[0]},
                 "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"}

        sec_k = {'privateExponent': secret_key[2], 'prime1': secret_key[0], 'prime2': secret_key[1],
                 'exponent1': secret_key[2] % (secret_key[0] - 1),
                 'exponent2': secret_key[2] % (secret_key[1] - 1),
                 'coefficient': self.__EucAlg(secret_key[0], secret_key[1])[2]}

        file = open(f"EncMsg - {date}.json", "w")
        json.dump(res, file, indent=4)
        file.close()

        file = open(f"PubKey - {date}.json", "w")
        json.dump(pub_k, file)
        file.close()

        file = open(f"SecKey - {date}.json", "w")
        json.dump(sec_k, file)
        file.close()

        pass

    @staticmethod
    def encrypt(pub_key: list[int, int], bytes_mess: bytes):
        _msg_len_bytes = len(bytes_mess)
        # print(f"Message len in bytes - {_msg_len_bytes}")
        # print(f"public key - {pub_key[0]}")
        # tt = pub_key[0].bit_length()
        # print(f"key bit len - {tt} | {tt // 8}")
        _key_byte_len = len(pub_key[0].to_bytes(math.ceil(math.log2(pub_key[0]) / 8), byteorder="big"))
        # y = math.log2(x)
        # math.ceil( y / 8 )
        #
        _block_len = _key_byte_len - 1
        _pad_bytes_size = math.ceil(math.log(_key_byte_len, 2) / 8)  # Нахожу размерность байтов для паддинга.
        # Округление в большую сторону кратность степени размера блока 8-ке
        # _pad_bytes_size = кратности степени размера блока 8-ке.

        # _key_byte_len = len(pub_key[0].to_bytes(pub_key[0].bit_length() // 8, byteorder="big")) # ( pub_key[0].bit_length() // 8 ) - размерность байт
        # print(f"key len in bytes - {_key_byte_len}")
        # print(f"Block len - {_block_len}")

        _msg_blocks = [bytes_mess[x:x + _block_len] for x in range(0, _msg_len_bytes, _block_len)]
        # print(f"Message blocks - {_msg_blocks}\nCount blocks - {len(_msg_blocks)}")
        # for i in _msg_blocks:
        # print(f"Len of one block - {len(i)}")
        # _block_len - len(_msg_blocks[-1])
        _count_pad = _block_len - len(_msg_blocks[-1])
        _padding_byte = (_count_pad).to_bytes(_pad_bytes_size, byteorder="big")
        # print(f"Byte to padding - {_padding_byte} | {len(_padding_byte)} | {_pad_bytes_size}")

        for i in range(_count_pad):
            _msg_blocks[-1] += _padding_byte

        for _block in _msg_blocks:
            # print(f"Len of one block - {len(i)}")
            # print(f"Num in block - {int.from_bytes(_block,byteorder= 'big')}")
            # print(int.from_bytes(_block,byteorder= 'big') < pub_key[0])

            pass
        # .to_bytes(_block_len, byteorder="big")
        #print(mp)
        return b"".join([x.to_bytes(math.ceil(math.log2(x) / 8), byteorder="big") for x in [
            pow(int.from_bytes(_block, byteorder='big'), pub_key[1], pub_key[0])
            for _block in _msg_blocks.copy()]])

    def pkcs_to_HumanSryle(self, path_msg: str, path_sk: str, path_pk: str):
        with open(path_msg, "r") as j_file:
            encrypted_msg = json.load(j_file)['EncryptedContentInfo']["encryptedContent"]

        with open(path_sk, "r") as j_file:
            res = json.load(j_file)
            sk_key = [res["SubjectPublicKeyInfo"]["N"], res["SubjectPublicKeyInfo"]["publicExponent"]]

        with open(path_pk, "r") as j_file:
            res = json.load(j_file)
            pk_key = [res["prime1"], res["prime2"], res["privateExponent"]]

        print(encrypted_msg)
        print(sk_key)
        print(pk_key)

        pass

    def decrypt(self, sec_key: list[int, int, int], encypted_msg: bytes):
        _msg_len_bytes = len(encypted_msg)
        _key_byte_len = len(
            (sec_key[0] * sec_key[1]).to_bytes(math.ceil(math.log2((sec_key[0] * sec_key[1])) / 8), byteorder="big"))
        # print(f"key len in bytes - {_key_byte_len}")
        _block_len = _key_byte_len - 1

        _encrypted_msg_blocks = [int.from_bytes(encypted_msg[x:x + _block_len+1], "big") for x in
                                 range(0, _msg_len_bytes, _block_len+1)]

        # decrypted_num = [pow(num, sec_key[2], sec_key[0] * sec_key[1]) for num in num_list]
        # print(_encrypted_msg_blocks)

        decrypted_msg = [x.to_bytes(_block_len, byteorder="big") for x in
                         [pow(num, sec_key[2], sec_key[0] * sec_key[1]) for num in _encrypted_msg_blocks]]

        _byte_check = decrypted_msg[-1][-1]
        checker = 0

        # print(len(decrypted_msg[-1][:_block_len - _byte_check]))
        # print(decrypted_msg[-1][:_block_len - _byte_check])
        decrypted_msg[-1] = decrypted_msg[-1][:_block_len - _byte_check]

        return b"".join(decrypted_msg)

    def __test_miller(self, flag: list):
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

    def __PrimeNum(self, k, t):
        def check(p):
            for i in range(t):
                if self.__test_miller([p, random.randint(2, p - 2)]) is True:
                    if i == t - 1:
                        return p
                    else:
                        continue
                else:
                    return False

        while True:
            prime = []
            for i in range(k):
                prime.append(str(round(random.random())))
            prime[0] = "1"
            prime[-1] = "1"
            p = int("".join(prime), 2)
            if check(p) is False:
                continue
            else:
                break
        # print(f"Prime number:\t\033[36m{p}\033[0m")
        return p

    def __EucAlg(self, x: int, y: int):
        if x >= y:
            pass
        elif x < y:
            mp = x
            x = y
            y = mp
        # BODY
        A = [0, 1]
        B = [1, 0]
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
        # print(f'NOD : {nod} | a : {a} | b : {b}')
        return nod, a, b


def rec_msg(path: str) -> str:
    with open(path_pk, "r") as file:
        pass


# print(pow(28678,7309,29987))
# print(pow(22703,20029,29987))
# for i in range(10):
#    print(timeit.timeit(lambda : cr.key_gen(512), number=1))

# print(timeit.timeit(lambda : RSA().key_gen(256), number= 10))
# print(timeit.timeit(lambda : ~-phi, number= 1000))
msg = "Когда теряет равновесие\n" \
      "Твое сознание усталое,\n" \
      "Когда ступеньки этой лестницы уход из-под ног\n" \
      "Как палуба,\n" \
      "Когда плюет на человечество твое ночное одиночество.\n" \
      "Ты можешь размышлять о вечности,".encode("utf-8")

cr = RSA()
sec, pub = cr.key_gen(512)

enc_msg = cr.encrypt(pub, msg)

print(len(msg))
print(len(enc_msg))
dec_msg = cr.decrypt(sec, enc_msg)

print(dec_msg.decode("utf-8") == msg.decode("utf-8"))


# r.pkcs_7_8_12(enc_mes, sec, pub)

# print(sec)

# print(pub)

path = "C:\\Users\\GEORG\\Desktop\\GEORG\\PythonWorks\\Crypto\\lab3\\EncMsg - 2022-04-03 17-49-23.json"
path_sk = "C:\\Users\\GEORG\\Desktop\\GEORG\\PythonWorks\\Crypto\\lab3\\PubKey - 2022-04-03 17-49-23.json"
path_pk = "C:\\Users\\GEORG\\Desktop\\GEORG\\PythonWorks\\Crypto\\lab3\\SecKey - 2022-04-03 17-49-23.json"

# cr.pkcs_to_HumanSryle(path, path_sk, path_pk)

# dec_mec = cr.decrypt(sec,enc_mes)
# print(enc_mes,"\n",dec_mec)

# {0, {ContentType, rsaEncryption, encryptedContent, OPTIONAL}}


"""
c = cr.encrypt(public_key)
print(f"Encrypt - {c}")
m = cr.decrypt(sec_key,c)
print((f"Decrypt - {m}"))
"""

"""
mess_bytes = "Yes comтётяmon fuПривет".encode("utf-8")
mess_by = "Yes comтётяmon fuПривет휌"#.encode("utf-8")

code_list = []
mp = mess_by.encode("utf-8").hex()

for i in [mess_by.encode("utf-8").hex()[x:x+2] for x in  range(0,len(mess_by.encode("utf-8").hex()),2)]:
    code_list.append(int(i,16))
print(mp)
print(code_list)
hex_str = ""
for i in code_list:
    hex_str += hex(i)[2:]

print(bytes.fromhex(hex_str).decode("utf-8"))


"""

"""
mp_list = []

for i in mess_by:
    #print(ord(i))
    if len(i.encode("utf-8").hex()) == 4:
        print('-------------------------------')
        print(int(i.encode("utf-8").hex()[:2],16))
        print(int(i.encode("utf-8").hex()[2:],16))
        print('-------------------------------')
print("+")
print(chr(1055))
print(len(bin(1103)[2:]))

bin_ = bin(int.from_bytes(mess_bytes, "big" ))[2:].zfill((len(mess_bytes.hex())//2)*8)

mes = bytes.fromhex(hex(int(bin_,2))[2:]).decode("utf-8")
print("=")
print(mes)
print(2**11)
count = 0
for i in range(pow(2,15)):
    print(chr(i), end=" ")
    if count == 64:
        count = 0
        print()
    count += 1
print("\n")
print(ord("휌"))
print(ord("н"))

print(chr(55052))
print(chr(53647))
print(chr(1085))

for i in [mess_by.encode("utf-8").hex()[x:x+2] for x in  range(0,len(mess_by.encode("utf-8").hex()),2)]:
    print(int(i,16))
print("е".encode("utf-8").hex())
print(bytes.fromhex("d0b5").decode("utf-8"))

print(bin(int("￠".encode("utf-8").hex(),16))[2:])
print("￠".encode("utf-8").hex())
npp = "111011111011111110100000"
npp = "0"*32 + npp
print(bytes.fromhex(hex(int(npp,2))[2:]).decode("utf-8"))
print(chr((2**16-32)))
"""

# Yes comтётяmon fuПривет
# 55052
