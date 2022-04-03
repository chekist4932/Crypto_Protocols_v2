import math
import random




DEFAULT_BLOCK_SIZE = 128 # Размер блока по умолчанию составляет 128 байт
BYTE_SIZE = 256 # 1 байт по умолчанию имеет 256 различных значений

def test_miller(flag:list):
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



def PrimeNum(k,t):
    def check(prime, p):
        for i in range(t):
            if test_miller([p, random.randint(2, p - 2)]) is True:
                if i == t - 1:
                    return p
                else:
                    continue
            else:
                return False

    while True:
        p = 0
        prime = []
        for i in range(k):
            prime.append(str(round(random.random())))
        prime[0] = "1"
        prime[-1] = "1"
        p = int("".join(prime),2)
        if check(prime,p) is False:
            continue
        else:
            break
    #print(f"Prime number:\t\033[36m{p}\033[0m")
    return p


def EucAlg(x: int,y: int):
    if x >= y:
        pass
    elif x < y:
        mp = x
        x = y
        y = mp
    # BODY
    A = [0,1]
    B = [1,0]
    while y != 0:
        q = x // y
        r = x - q*y
        a = A[1] - q * A[0]
        b = B[1] - q*B[0]
        x = y
        y = r
        A[1] = A[0]
        A[0] = a
        B[1] = B[0]
        B[0] = b
        nod = x
        a = A[1]
        b = B[1]
    #print(f'NOD : {nod} | a : {a} | b : {b}')
    return nod,a,b


def mess_bytes_to_bin(mess_bytes: bytes): # encoding utf-8
    num_list = []
    bin_mess = bin(int.from_bytes(mess_bytes, "big"))[2:].zfill((len(mess_bytes.hex()) // 2) * 8)

    octet_count = 0
    while True:
        if len(bin_mess) < 512:
            for i in [bin_mess[x:x+8] for x in range(0,len(bin_mess),8)]:
                octet_count += 1
            bin_mess =   "00000000" * ( (64-octet_count) % 63) + bin_mess
            num_list.append(int(bin_mess, 2))
            break
        else:
            num_list.append(int(bin_mess[:512],2))
            bin_mess = bin_mess[512:]

    return num_list
    #print(bin_mess)


"""
rsa = RSA()
sec, pub = rsa.key_gen(512)
c = rsa.encrypt(pub,num_list)
m = rsa.decrypt(sec,c)
print(c)
print(m)
print(m == num_list)
res_ = ""
for i in m:
    res_ += bin(i)[2:].zfill(512)

MES_array = [hex(int(res_[i:i + 8],2))[2:] for i in range(0, len(res_), 8)]

print(bytes.fromhex("".join(MES_array)).decode("utf-8"))
"""
def padding_msg(msg_bytes: bytes, pub_key: list[int, int]):
    byte_len = len(pub_key[0].to_bytes(pub_key[0].bit_length() // 8, byteorder="big"))
    print(byte_len)

"""
mess = "abcdefghqwertyuiopasdfzxcvbnmhвпвлоывладвыоашыглаорвыитаоыбфтащуцшг43ег5н43094егруашлтывлваоыьдфытаыфб"

mess_b= mess.encode("utf-8")
rsa = RSA()
sec, pub = rsa.key_gen(512)
padding_msg(mess_b,pub)
"""
mes = "hell".encode("utf-8").hex()
mess = bytes.fromhex(mes).decode("utf-8")
print(mess)
print(2**24)
print(math.ceil(math.log(2048,2)  / 8),"\n")
tt = b'\x1e'
print(int.from_bytes(tt,"big"))



"""
_msg_len_bytes = len(encypted_msg)
        _key_byte_len = len(
            (sec_key[0] * sec_key[1]).to_bytes(math.ceil(math.log2((sec_key[0] * sec_key[1])) / 8), byteorder="big"))
        # print(f"key len in bytes - {_key_byte_len}")
        _block_len = _key_byte_len - 1

        _encrypted_msg_blocks = [int.from_bytes(encypted_msg[x:x + _block_len], "big") for x in
                                 range(0, _msg_len_bytes, _block_len)]

        # decrypted_num = [pow(num, sec_key[2], sec_key[0] * sec_key[1]) for num in num_list]

        decrypted_msg = [x.to_bytes(_block_len, byteorder="big") for x in
                         [pow(num, sec_key[2], sec_key[0] * sec_key[1]) for num in _encrypted_msg_blocks]]

        _byte_check = decrypted_msg[-1][-1]
        checker = 0

"""