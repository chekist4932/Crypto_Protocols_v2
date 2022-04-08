import timeit
import random
import math

import json
import datetime


class RSA:
    def __init__(self):
        self.data = str(datetime.datetime.now())[:-7].replace(":", "-")
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

    @staticmethod
    def encrypt(pub_key: list[int, int], bytes_mess: bytes):
        _msg_len_bytes = len(bytes_mess)
        _key_byte_len = len(pub_key[0].to_bytes(math.ceil(math.log2(pub_key[0]) / 8), byteorder="big"))
        # y = math.log2(x)
        # math.ceil( y / 8 )
        #
        _block_len = _key_byte_len - 1
        _pad_bytes_size = math.ceil(math.log(_key_byte_len, 2) / 8)  # Нахожу размерность байтов для паддинга.
        # Округление в большую сторону кратность степени размера блока 8-ке
        # _pad_bytes_size = кратности степени размера блока 8-ке.

        _msg_blocks = [bytes_mess[x:x + _block_len] for x in range(0, _msg_len_bytes, _block_len)]

        _count_pad = _block_len - len(_msg_blocks[-1])
        _padding_byte = (_count_pad).to_bytes(_pad_bytes_size, byteorder="big")

        for i in range(_count_pad):
            _msg_blocks[-1] += _padding_byte

        return b"".join([x.to_bytes(math.ceil(math.log2(x) / 8), byteorder="big") for x in [
            pow(int.from_bytes(_block, byteorder='big'), pub_key[1], pub_key[0])
            for _block in _msg_blocks.copy()]])

    def decrypt(self, sec_key: list[int, int, int], encrypted_msg: bytes):

        _msg_len_bytes = len(encrypted_msg)
        _key_byte_len = len(
            (sec_key[0] * sec_key[1]).to_bytes(math.ceil(math.log2((sec_key[0] * sec_key[1])) / 8), byteorder="big"))
        _block_len = _key_byte_len - 1

        _encrypted_msg_blocks = [int.from_bytes(encrypted_msg[x:x + _block_len + 1], "big") for x in
                                 range(0, _msg_len_bytes, _block_len + 1)]

        decrypted_msg = [x.to_bytes(_block_len, byteorder="big") for x in
                         [pow(num, sec_key[2], sec_key[0] * sec_key[1]) for num in _encrypted_msg_blocks]]

        _byte_check = decrypted_msg[-1][-1]
        __checker = 0
        print(_byte_check)
        for i in range(len(decrypted_msg[-1])-1, (_block_len - _byte_check)-1, -1):
            print(i)
            if decrypted_msg[-1][i] == _byte_check:
                __checker += 1
        print(__checker)
        # input()
        if __checker == _byte_check:
            decrypted_msg[-1] = decrypted_msg[-1][:_block_len - _byte_check]
            return b"".join(decrypted_msg)
        else:
            raise ValueError("Wrong key")




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

    def __PrimeNum_arch(self, k, t):
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
        return p

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

    def pkcs_8_12(self, secret_key: list[int], public_key: list[int], date):
        # encr = [x.to_bytes(math.ceil(math.log2(x) / 8), byteorder="big").hex() for x in encrypted_msg]
        # date = str(datetime.datetime.now())[:-7].replace(":", "-")

        pub_k = {"SubjectPublicKeyInfo": {"publicExponent": public_key[1], "N": public_key[0]},
                 "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"}

        sec_k = {'privateExponent': secret_key[2], 'prime1': secret_key[0], 'prime2': secret_key[1],
                 'exponent1': secret_key[2] % (secret_key[0] - 1),
                 'exponent2': secret_key[2] % (secret_key[1] - 1),
                 'coefficient': self.__EucAlg(secret_key[0], secret_key[1])[2]}

        file = open(f"results\\PubKey - {date}.json", "w")
        json.dump(pub_k, file)
        file.close()

        file = open(f"results\\SecKey - {date}.json", "w")
        json.dump(sec_k, file)
        file.close()

    def pkcs_7_int(self, encrypted_msg: list[int], date):
        res = {"Version": 0,
               "EncryptedContentInfo":
                   {"ContentType": "text",
                    "ContentEncryptionAlgorithmIdentifier": "rsaEncryption",
                    "encryptedContent": "".join(
                        [x.to_bytes(math.ceil(math.log2(x) / 8), byteorder="big").hex() for x in encrypted_msg]),
                    "OPTIONAL": "NULL"}}
        file = open(f"results\\EncMsg - {date}.json", "w")
        json.dump(res, file, indent=4)
        file.close()

    def pkcs_7_bytes(self, encrypted_msg: bytes, date):
        res = {"Version": 0,
               "EncryptedContentInfo":
                   {"ContentType": "text",
                    "ContentEncryptionAlgorithmIdentifier": "rsaEncryption",
                    "encryptedContent": encrypted_msg.hex(),
                    "OPTIONAL": "NULL"}}
        file = open(f"results\\EncMsg - {date}.json", "w")
        json.dump(res, file, indent=4)
        file.close()

    def read_out_file(self, path: str, mode: str):
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


# print(pow(28678,7309,29987))
# print(pow(22703,20029,29987))
# for i in range(10):
#    print(timeit.timeit(lambda : cr.key_gen(512), number=1))

# print(timeit.timeit(lambda : RSA().key_gen(256), number= 10))
# print(timeit.timeit(lambda : ~-phi, number= 1000))

"""

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

print(math.log2(515).is_integer())
"""
# r.pkcs_7_8_12(enc_mes, sec, pub)

# print(sec)

# print(pub)


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
