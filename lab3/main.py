# Меню лабораторной работы №3. "Реализация RSA согласно стандартов PKCS 7, PKCS 8, PKCS 12".
import math
import datetime
import my_rsa

def path_getter(mode):
    while True:
        try:
            path = input(f"Input path to {mode}:\n-\t")
        except Exception as err:
            print(f"Uncorrect path. {err}.")
            continue
        else:
            return path



def menu():
    while True:
        # date = str(datetime.datetime.now())[:-7].replace(":", "-")
        try:
            choose = int(
                input("\n1.\tGeneration pair (secret,public) keys.\n2.\tEncrypt.\n3.\tDecrypt.\n4.\tExit.\n-\t"))
        except Exception:
            print("Input error. Try again!")
            continue
        else:
            if choose == 1:  # generation keys
                while True:
                    try:
                        key_digit = int(input("Input keysize (The number must be a power of two and > 512):\n"))
                    except Exception:
                        print("Input error. Try again!")
                        continue
                    else:
                        if key_digit < 512:
                            print("Input error. Number < 512. Try again!")
                            continue
                        elif not math.log2(key_digit).is_integer():
                            print("Input error. The number is not a power of two. Try again!")
                            continue
                        else:
                            break
                print("\nKey pair generation in progress\n")
                cr = my_rsa.RSA()
                sec, pub = cr.key_gen(key_digit)
                cr.pkcs_8_12(sec, pub, cr.data)
                print("\n\033[36mKey pair generated.\033[0m\n")
            elif choose == 2:  # encryption
                while True:
                    path_msg = path_getter("msg")
                    try:
                        msg = my_rsa.RSA().read_out_file(path_msg, "msg").encode("utf-8")
                    except Exception as err:
                        print(f"Input error. Try again!. {err}")
                        continue
                    else:
                        while True:
                            path = path_getter("public key")
                            try:
                                pub_key = my_rsa.RSA().read_out_file(path, "pb")
                            except Exception as err:
                                print(f"Input error. Try again!. {err}")
                                continue
                            else:
                                print("\nEncryption in progress\n")
                                try:
                                    encrypted_msg = my_rsa.RSA().encrypt(pub_key,msg)
                                except ValueError as err:
                                    print(f"Input error. Try again!. {err}")
                                    continue
                                else:
                                    my_rsa.RSA().pkcs_7_bytes(encrypted_msg,my_rsa.RSA().data)
                                    print("\n\033[36mEncryption completed.\033[0m\n")
                                    break
                        break


                pass
            elif choose == 3:  # decryption
                while True:
                    path_encr = path_getter("encrypted msg")
                    try:
                        encr = bytes.fromhex(my_rsa.RSA().read_out_file(path_encr,"en_msg"))
                    except Exception as err:
                        print(f"Input error. Try again!. {err}")
                        continue
                    else:
                        while True:
                            path_sc = path_getter("secret key")
                            try:
                                sec_key = my_rsa.RSA().read_out_file(path_sc, "sc")
                            except Exception as err:
                                print(f"Input error. Try again!. {err}")
                                continue
                            else:
                                print("\nDecryption in progress\n")
                                decrypted_msg = my_rsa.RSA().decrypt(sec_key,encr)
                                print("\n\033[36mEncryption completed.\033[0m\n")
                                print(decrypted_msg.decode("utf-8"))
                                with open(f"results\\DecMsg - {my_rsa.RSA().data}", "w", encoding="utf-8") as file:
                                    file.write(decrypted_msg.decode("utf-8"))
                                break
                    break


                pass
            elif choose == 4:  # exit
                break
    pass


menu()


# C:\Users\GEORG\Desktop\GEORG\PythonWorks\Crypto\lab3\msg.txt
# C:\Users\GEORG\Desktop\GEORG\PythonWorks\Crypto\lab3\results\PubKey - 2022-04-08 10-23-28.json
# C:\Users\GEORG\Desktop\GEORG\PythonWorks\Crypto\lab3\results\SecKey - 2022-04-08 10-23-28.json
# C:\Users\GEORG\Desktop\GEORG\PythonWorks\Crypto\lab3\results\EncMsg - 2022-04-08 10-24-30.json
