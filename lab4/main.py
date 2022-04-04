# Хеш-функция ГОСТ Р 34.11-2012 "Стрибог"
import math
import LPS


def get_msg():
    while True:
        choose = input("1.\t512 bit\n2.\t256 bit\n-\t")
        if choose == "1":
            Layout = 512
            break
        elif choose == "2":
            Layout = 256
            break
        else:
            print("Input error. Try again.")
            continue

    while True:
        choose = input("Iput:\n1.\tKeyboard\n2.\tFile\n-\t")
        if choose == "1":
            mes = input("\nInput your message:\n-\t")
            # Msg_bin = bin(int.from_bytes(mes.encode("utf-8"), "little"))[2:].zfill(
            #   (len(mes.encode("utf-8").hex()) // 2) * 8)
            # Msg = mes.encode("utf-8")
            Msg = bytearray(mes.encode("utf-8"))
            Msg.reverse()
            Msg = bytes(Msg)
            return Msg, Layout
        elif choose == "2":
            while True:
                print("\nInput mess in lab4\\mes.txt")
                mp_choose = input("1.\tGo\n-\t")
                if mp_choose == "1":
                    try:
                        file = open("mes.txt", encoding="utf-8")
                        mes = file.read()
                        file.close()
                        Msg = bytearray(mes.encode("utf-8"))
                        Msg.reverse()
                        Msg = bytes(Msg)

                    except Exception as err:
                        print(err)
                        continue
                    else:
                        return Msg, Layout
                else:
                    print("Input error. Try again.")
                    continue
            break
        else:
            print("Input error. Try again.")
            continue


def gost34122012(Msg: bytes, Layout: int):
    if Layout == 512:
        hash_ = b'\x00' * 64

    elif Layout == 256:
        hash_ = b'\x01' * 64

    N_vector = b'\x00' * 64
    E_vector = b'\x00' * 64

    big_lit = "big"

    while True:
        if len(Msg) < 64:
            Len_Msg = len(Msg)
            Msg = (b"\x00" * (63 - Len_Msg)) + b"\x01" + Msg
            hash_ = LPS.g_N(hash_, Msg, N_vector)

            n_num = (int(N_vector.hex(), 16) + (Len_Msg * 8)) % pow(2, 512)
            mp = n_num.to_bytes(math.ceil(math.log2(n_num) / 8), big_lit)
            N_vector = (b"\x00" * (64 - len(mp))) + mp

            e_num = (int(E_vector.hex(), 16) + int(Msg.hex(), 16)) % pow(2, 512)
            mp = e_num.to_bytes(math.ceil(math.log2(e_num) / 8), big_lit)
            E_vector = (b"\x00" * (64 - len(mp))) + mp

            Zero_vector = b'\x00' * 64
            hash_ = LPS.g_N(hash_, N_vector, Zero_vector)

            if Layout == 512:
                hash_ = LPS.g_N(hash_, E_vector, Zero_vector)
            elif Layout == 256:
                hash_ = LPS.g_N(hash_, E_vector, Zero_vector)[:32]

            result = bytearray(hash_)
            result.reverse()
            return bytes(result).hex()
            # break
        else:
            Mp_Msg = Msg
            mod_pr = len(Msg)
            Msg = Mp_Msg[mod_pr - 64:]
            hash_ = LPS.g_N(hash_, Msg, N_vector)

            n_num = (int(N_vector.hex(), 16) + 512) % pow(2, 512)
            mp = n_num.to_bytes(math.ceil(math.log2(n_num) / 8), big_lit)
            N_vector = (b"\x00" * (64 - len(mp))) + mp

            e_num = (int(E_vector.hex(), 16) + int(Msg.hex(), 16)) % pow(2, 512)
            mp = e_num.to_bytes(math.ceil(math.log2(e_num) / 8), big_lit)
            E_vector = (b"\x00" * (64 - len(mp))) + mp

            Msg = Mp_Msg[:mod_pr - 64]


if __name__ == '__main__':
    Msg, Layout = get_msg()
    print(gost34122012(Msg, Layout))
