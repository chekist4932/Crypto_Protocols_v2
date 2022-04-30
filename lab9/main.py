# Лабораторная работа №9
# Цифровая подпись Фиата-Шамира


import json
import math
from datetime import datetime

import lab9_client
import GOST_R_34_12_2012
import Fiat
import sha_256_512


def check(SetOfAt: dict, hash_type: str):
    user_sign = bytes.fromhex(SetOfAt["UserSignature"])
    tms = json.dumps(SetOfAt["Timestamp"]).encode()

    center_signature = SetOfAt["CenterSignature"]

    center_pub_key = SetOfAt["CenterSubjectPublicKeyInfo"]["SubjectPublicKeyInfo"]

    return Fiat.Shamir().check_signature(center_pub_key, center_signature, user_sign+tms, hash_type)


def show_res(res_dict: dict):
    print(f"Hash type:\t{res_dict['DigestAlgorithmIdentifiers']}")
    print(
        f"Alg signature:\t{res_dict['SignerInfos']['SignatureAlgorithmIdentifier']}")
    print(f"Author signature:\t{res_dict['SignerInfos']['SignerIdentifier']}")
    print(
        f"UTCTime:\t{res_dict['SignerInfos']['UnsignedAttributes']['SET OF AttributeValue']['Timestamp']['UTCTime']}")
    print(
        f"Time of center:\t{res_dict['SignerInfos']['UnsignedAttributes']['SET OF AttributeValue']['Timestamp']['GeneralizedTime']}")


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
        path_msg = path_getter(mode)
        try:
            msg = Fiat.Shamir().read_out_file(path_msg, mode)
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
                        key_digit = int(input("Input keysize (The number must be a power of two and >= 512):\n"))
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
                            size_choice = input("Select hash size:\n1.\t256\n2.\t512\n-\t")
                            if size_choice == "1" or size_choice == '2':
                                size_ = (256 if size_choice == "1" else 512)
                                break
                            else:
                                print("Again.")
                                continue

                print("\nKey pair generation in progress\n")
                cr = Fiat.Shamir()
                sec, pub = cr.key_gen(key_digit, size_)
                cr.pkcs_8_12(sec, pub, cr.data)
                print("\n\033[36mKey pair generated.\033[0m\n")
            elif choose == 2:  # encryption
                while True:

                    msg: bytes = open_file("msg")
                    pub_key: dict = open_file("pb")
                    sec_key: dict = open_file("sk")
                    # size_ = math.ceil(math.log2(sec_key['prime1']))
                    size_ = len(sec_key['privateExponent'])
                    while True:
                        hash_choice = input("Select hash alg:\n1.\tSHA\n2.\tGOST R 34.11-2012\n-\t")
                        # size_choice = input("Select size:\n1.\t256\n2.\t512\n-\t")
                        # if size_choice == "1" or size_choice == '2':
                        #     size_ = (256 if size_choice == "1" else 512)
                        # else:
                        #     print("Again.")
                        #     continue
                        if hash_choice == "1":
                            hash_type = "sha" + str(size_)
                            break
                        elif hash_choice == "2":
                            hash_type = "GOST" + str(size_)
                            break
                        else:
                            print("Again.")
                            continue

                    print("\n\033[36mSignature in progress.\033[0m\n")
                    try:
                        local_signature: dict = Fiat.Shamir().signature(sec_key, msg, hash_type)
                    except ValueError as err:
                        print(f"Input error. Try again!. {err}")
                        continue
                    else:
                        # ЗАПИСЬ ПО PKCS 7
                        time_mark = str(datetime.now())[2:-7].replace("-", "-").replace(" ",
                                                                                        "-").replace(
                            ":", "-")
                        signature_PKCS: dict = Fiat.Shamir().PKCS_7_CAdES(msg.hex(), local_signature,
                                                                   hash_type, pub_key, time_mark)

                        input("Enter for send to Time Stamp Center\n-\t")

                        with open(f"results\\Signature {time_mark}.json", "r", encoding="utf-8") as j_f:
                            signature_PKCS = json.load(j_f)

                        if not lab9_client.client(signature_PKCS):
                            print("Error in Time Stamp Center")
                            break
                        else:
                            res_time_center = lab9_client.client(signature_PKCS)
                            SetOfAttr = json.loads(res_time_center.decode())

                            flag_check = check(SetOfAttr, hash_type)

                            if flag_check:

                                file = open(f"results\\Signature {time_mark}.json", "r", encoding="utf-8")
                                res_dict = json.load(file)
                                file.close()
                                file = open(f"results\\Signature {time_mark}.json", "w", encoding="utf-8")
                                res_dict["SignerInfos"]["UnsignedAttributes"][
                                    "SET OF AttributeValue"] = SetOfAttr
                                json.dump(res_dict, file, indent=4)
                                file.close()
                                print("Timestamp is CORRECT\n")
                                show_res(res_dict)
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

# msg.txt
# results/PubKey - 2022-04-30 15-53-24.json
# results/SecKey - 2022-04-30 15-53-24.json
