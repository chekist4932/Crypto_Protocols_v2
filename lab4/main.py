# Хеш-функция ГОСТ Р 34.11-2012 "Стрибог"


import LPS


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
