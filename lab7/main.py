# Меню лабораторной работы №3. "Реализация RSA согласно стандартов PKCS 7, PKCS 8, PKCS 12".
import json
import math
from datetime import datetime

import GOST_R_34_12_2012
import lab7_client
import my_rsa
import sha_256_512


def check(SetOfAt: dict):
    user_sign = SetOfAt["UserSignature"]
    tms = json.dumps(SetOfAt["Timestamp"]).encode()

    enc_center_signature = SetOfAt["CenterSignature"]

    center_pub_key = [SetOfAt["CenterSubjectPublicKeyInfo"]["SubjectPublicKeyInfo"]["N"],
                      SetOfAt["CenterSubjectPublicKeyInfo"]["SubjectPublicKeyInfo"]["publicExponent"]
                      ]

    decrypt_center_signature = my_rsa.RSA().decrypt(center_pub_key, bytes.fromhex(enc_center_signature))

    if decrypt_center_signature.hex() == (user_sign + tms.hex()):
        return True
    else:
        return False


def path_getter(mode):
    while True:
        try:
            path = input(f"Input path to {mode}:\n-\t")
            file = open(path)
        except Exception as err:
            print(f"Uncorrect path. {err}.")
            continue
        else:
            file.close()
            return path


def open_file(mode: str):
    while True:
        path_msg = path_getter("msg")
        try:
            msg = my_rsa.RSA().read_out_file(path_msg, "msg").encode("utf-8")
        except Exception as err:
            print(f"Input error. Try again!. {err}")
            continue
        else:
            return msg
    pass


def menu():
    while True:
        # date = str(datetime.datetime.now())[:-7].replace(":", "-")
        try:
            choose = int(
                input("\n1.\tGeneration pair (secret,public) keys.\n2.\tSignature.\n3.\tExit.\n-\t"))
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

                    msg = open_file("msg")
                    pub_key = open_file("pb")
                    sec_key = open_file("sk")
                    pkcs_pub_key = {"SubjectPublicKeyInfo": {"publicExponent": pub_key[1], "N": pub_key[0]},
                             "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"}

                    while True:
                        hash_choice = input("Select hash alg:\n1.\tSHA\n2.\tGOST R 34.11-2012\n-\t")
                        size_choice = input("Select size:\n1.\t256\n2.\t512\n-\t")
                        if size_choice == "1" or size_choice == '2':
                            size_ = (256 if size_choice == "1" else 512)
                        else:
                            print("Again.")
                            continue

                        if hash_choice == "1":
                            hash_msg = sha_256_512.sha_(msg, size_)
                            hash_type = "sha" + str(size_)
                            break
                        elif hash_choice == "2":
                            hash_msg = GOST_R_34_12_2012.GOST_34_11_2012(msg, size_).hash_()
                            hash_type = "GOST" + str(size_)
                            break
                        else:
                            print("Again.")
                            continue

                    print("\n\033[36mSignature in progress.\033[0m\n")
                    try:
                        user_signature = my_rsa.RSA().encrypt([sec_key[0] * sec_key[1], sec_key[2]],
                                                              hash_msg)
                    except ValueError as err:
                        print(f"Input error. Try again!. {err}")
                        continue
                    else:
                        # ЗАПИСЬ ПО PKCS 7
                        time_mark = str(datetime.now())[2:-7].replace("-", "-").replace(" ",
                                                                                        "-").replace(
                            ":", "-")
                        sign_dict = my_rsa.RSA().PKCS_7_CAdES(msg.hex(), user_signature.hex(),
                                                              hash_type, pkcs_pub_key, time_mark)

                        input("Enter for send to Time Stamp Center\n-\t")

                        with open(f"results\\Signature {time_mark}.json", "r", encoding="utf-8") as jf:
                            sign_dict = json.load(jf)

                        if lab7_client.client(sign_dict) == False:
                            print("Error in Time Stamp Center")
                            break
                        else:
                            res_time_center = lab7_client.client(sign_dict)
                            SetOfAttr = json.loads(res_time_center.decode())
                            flag_check = check(SetOfAttr)
                            if flag_check == True:

                                file = open(f"results\\Signature {time_mark}.json", "r", encoding="utf-8")
                                res_dict = json.load(file)
                                file.close()
                                file = open(f"results\\Signature {time_mark}.json", "w", encoding="utf-8")
                                res_dict["SignerInfos"]["UnsignedAttributes"][
                                    "SET OF AttributeValue"] = SetOfAttr
                                json.dump(res_dict, file, indent=4)
                                file.close()
                                print("Timestamp is CORRECT\n")
                                print(f"Hash type:\t{res_dict['DigestAlgorithmIdentifiers']}")
                                print(
                                    f"Alg signature:\t{res_dict['SignerInfos']['SignatureAlgorithmIdentifier']}")
                                print(f"Author signature:\t{res_dict['SignerInfos']['SignerIdentifier']}")
                                print(
                                    f"UTCTime:\t{res_dict['SignerInfos']['UnsignedAttributes']['SET OF AttributeValue']['Timestamp']['UTCTime']}")
                                print(
                                    f"Time of center:\t{res_dict['SignerInfos']['UnsignedAttributes']['SET OF AttributeValue']['Timestamp']['GeneralizedTime']}")
                                print("\n\033[36mSignature completed.\033[0m\n")

                            else:
                                print("Error in Time Stamp Center")
                            break

            elif choose == 3:  # exit
                break
            else:
                print(f"Incorrect input.")
                continue

    pass


menu()

# C:\Users\GEORG\Desktop\GEORG\PythonWorks\Crypto\lab7\msg.txt
# C:\Users\GEORG\Desktop\GEORG\PythonWorks\Crypto\lab7\results\PubKey - 2022-04-21 14-43-32.json
# C:\Users\GEORG\Desktop\GEORG\PythonWorks\Crypto\lab7\results\SecKey - 2022-04-21 14-43-32.json
