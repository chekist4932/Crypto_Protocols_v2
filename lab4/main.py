# Хеш-функция ГОСТ Р 34.11-2012 "Стрибог"
import LPS
import codecs
import copy
def text_to_bin(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    #while len(bits) % 8 != 0:
        #bits = "0" + bits
    return bits

def text_from_bin(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'



def stribog():

     while True:
          try:
               choose = int(input("1.\t512 bit\n2.\t256 bit\n-\t"))
          except Exception:
               print("Input error. Try again.")
               continue
          else:
               if choose == 1:
                    mod = 512
                    break
               elif choose == 2:
                    mod = 256
                    break
               else:
                    print("Input error. Try again.")
                    continue

     while True:
          try:
               choose = int(input("Iput:\n1.\tFile\n2.\tKeyboard\n-\t"))
          except Exception:
               print("Input error. Try again.")
               continue
          else:
               if choose == 1:
                    while True:
                         print("\nInput mess in mes.txt")
                         try:
                              mp_choose = int(input("1.\tMes in hex\n2.\tMes in Unicod\n-\t"))
                         except Exception:
                              print("Input error. Try again.")
                              continue
                         else:
                              if mp_choose == 1:
                                   file = open("mes.txt", encoding="utf-8")
                                   mes = file.read()
                                   file.close()
                                   break
                              elif mp_choose == 2:
                                   file = open("mes.txt", encoding="utf-8")
                                   mes = file.read()
                                   file.close()
                                   ####
                                   mp = mes.encode("utf-8").hex()
                                   mes = [mp[x:x+2] for x in range(0,len(mp),2)]
                                   mes.reverse()
                                   mes = "".join(mes)
                                   #mes = mes.encode("utf-8").hex()[::-1]
                                   break
                              else:
                                   print("Input error. Try again.")
                                   continue
                    break
               elif choose == 2:
                    while True:
                         print("\nInput mes:")
                         try:
                              mp_choose = int(input("1.\tMes in hex\n2.\tMes in Unicod\n-\t"))
                         except Exception:
                              print("Input error. Try again.")
                              continue
                         else:
                              if mp_choose == 1:

                                   mes = input("Input your message:\n-\t")

                                   break
                              elif mp_choose == 2:
                                   mes = input("Input your message:\n-\t")
                                   #mes = mes[::-1].encode("cp1251").hex()
                                   mp = mes.encode("utf-8").hex()
                                   mes = [mp[x:x + 2] for x in range(0, len(mp), 2)]
                                   mes.reverse()
                                   mes = "".join(mes)


                                   break
                              else:
                                   print("Input error. Try again.")
                                   continue
                    break
               else:
                    print("Input error. Try again.")
                    continue


     m = LPS.hex_to_bin(mes)




     # if верстка 512 бит
     if mod == 512:
          h = "0" * 512

     elif mod == 256:
          h = "00000001" * 64

     N = "0" * 512
     E = "0" * 512

     while True:
          if len(m) < 512:
               mod_prime = len(m)
               m = ("0" * (511 - mod_prime)) + '1' + m

               # print(LPS.bin_to_hex(m))
               h = LPS.g_N(h, m, N)
               N = bin((int(N, 2) + mod_prime) % 2 ** 512)[2:]
               while len(N) % 512 != 0:
                    N = "0" + N
               E = bin((int(E, 2) + int(m, 2)) % 2 ** 512)[2:]
               while len(E) % 512 != 0:
                    E = "0" + E

               o = "0" * 512
               h = LPS.g_N(h, N, o)
               if mod == 512:
                    h = LPS.g_N(h, E, o)
               elif mod == 256:
                    h = LPS.g_N(h, E, o)[:256]


               if mp_choose == 1:
                    print(LPS.bin_to_hex(h))
               elif mp_choose == 2:
                    new = ""
                    for i in [LPS.bin_to_hex(h)[i:i + 2] for i in range(0, len(LPS.bin_to_hex(h)), 2)]:
                         new += i[::-1]
                    print(new[::-1])



               break
          else:
               mp_m = m
               mod_pr = len(m)
               m = mp_m[mod_pr - 512:]
               h = LPS.g_N(h, m, N)
               N = bin((int(N, 2) + 512) % 2 ** 512)[2:]
               while len(N) % 512 != 0:
                    N = "0" + N
               E = bin((int(E, 2) + int(m, 2)) % 2 ** 512)[2:]
               while len(E) % 512 != 0:
                    E = "0" + E
               m = mp_m[:mod_pr - 512]



stribog()


"00557be5e584fd52a449b16b0251d05d27f94ab76cbaa6da890b59d8ef1e159d" # контр пример 1 в госте 256 верстка
"00557be5e584fd52a449b16b0251d05d27f94ab76cbaa6da890b59d8ef1e159d" # работа моего кода

"28fbc9bada033b1460642bdcddb90c3fb3e56c497ccd0f62b8a2ad4935e85f037613966de4ee00531ae60f3b5a47f" \
"8dae06915d5f2f194996fcabf2622e6881e" # контр пример 2 в госте
"28fbc9bada033b1460642bdcddb90c3fb3e56c497ccd0f62b8a2ad4935e85f037613966de4ee00531ae60f3b5a47f" \
"8dae06915d5f2f194996fcabf2622e6881e" # работа моего кода


# Fist example '323130393837363534333231303938373635343332313039383736353433323130393837363534333231303938373635343332313039383736353433323130'
# Second example "fbe2e5f0eee3c820fbeafaebef20fffbf0e1e0f0f520e0ed20e8ece0ebe5f0f2f120fff0eeec20f120faf2fee5e2202ce8f6f3ede220e8e6eee1e8f0f2d1202ce8f0f2e5e220e5d1"

"508f7e553c06501d749a66fc28c6cac0b005746d97537fa85d9e40904efed29d"
"508f7e553c06501d749a66fc28c6cac0b005746d97537fa85d9e40904efed29d"
