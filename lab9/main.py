# Лабораторная работа №9
# Цифровая подпись Фиата-Шамира


import json
import math
from datetime import datetime

import lab9_client
import GOST_R_34_12_2012
import Fiat
import sha_256_512


def check(set_of_attr: dict, hash_type: str):
    user_sign = bytes.fromhex(set_of_attr["UserSignature"])
    tms = json.dumps(set_of_attr["Timestamp"]).encode()

    center_signature = set_of_attr["CenterSignature"]

    center_pub_key = set_of_attr["CenterSubjectPublicKeyInfo"]["SubjectPublicKeyInfo"]

    return Fiat.Shamir().check_signature(center_pub_key, center_signature, user_sign + tms, hash_type)


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
            print(f"Incorrect path. {err}.")
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

def get_hash_type(size_):
    while True:
        hash_choice = input("Select hash alg:\n1.\tSHA\n2.\tGOST R 34.11-2012\n-\t")
        if hash_choice == "1":
            return "sha" + str(size_)
        elif hash_choice == "2":
            return "GOST" + str(size_)
        else:
            print("Again.")

def signature():
    while True:
        msg: bytes = open_file("msg")
        pub_key: dict = open_file("pb")
        sec_key: dict = open_file("sk")
        size_ = len(sec_key['privateExponent'])
        hash_type = get_hash_type(size_)
        print("\n\033[36mSignature in progress.\033[0m\n")
        try:
            local_signature: dict = Fiat.Shamir().signature(sec_key, msg, hash_type)
        except ValueError as err:
            print(f"Input error. Try again!. {err}")
        else:
            # ЗАПИСЬ ПО PKCS 7
            time_mark = str(datetime.now())[2:-7].replace("-", "-").replace(" ",
                                                                            "-").replace(
                ":", "-")
            signature_pkcs: dict = Fiat.Shamir().PKCS_7_CAdES(msg.hex(), local_signature,
                                                              hash_type, pub_key, time_mark)

            input("Enter for send to Time Stamp Center\n-\t")

            with open(f"results\\Signature {time_mark}.json", "r", encoding="utf-8") as j_f:
                signature_pkcs = json.load(j_f)

            if not lab9_client.client(signature_pkcs):
                print("Error in Time Stamp Center")
                break
            else:
                res_time_center = lab9_client.client(signature_pkcs)
                set_of_attr = json.loads(res_time_center.decode())

                flag_check = check(set_of_attr, hash_type)

                if flag_check:

                    file = open(f"results\\Signature {time_mark}.json", "r", encoding="utf-8")
                    res_dict = json.load(file)
                    file.close()
                    file = open(f"results\\Signature {time_mark}.json", "w", encoding="utf-8")
                    res_dict["SignerInfos"]["UnsignedAttributes"][
                        "SET OF AttributeValue"] = set_of_attr
                    json.dump(res_dict, file, indent=4)
                    file.close()
                    print("Timestamp is CORRECT\n")
                    show_res(res_dict)
                    print("\n\033[36mSignature completed.\033[0m\n")

                else:
                    print("Error in Time Stamp Center")
                break


def gen_keys():
    while True:
        try:
            key_digit = int(input("Input keysize (The number must be a power of two and >= 512):\n"))
            if key_digit < 512:
                print("Input error. Number < 512. Try again!")
            elif not math.log2(key_digit).is_integer():
                print("Input error. The number is not a power of two. Try again!")
            else:
                size_choice = input("Select hash size:\n1.\t256\n2.\t512\n-\t")
                if size_choice == "1" or size_choice == '2':
                    size_ = (256 if size_choice == "1" else 512)
                    break
                else:
                    print("Again.")
        except Exception:
            print("Input error. Try again!")

    print("\nKey pair generation in progress\n")
    cr = Fiat.Shamir()
    sec, pub = cr.key_gen(key_digit, size_)
    cr.pkcs_8_12(sec, pub, cr.data)
    print("\n\033[36mKey pair generated.\033[0m\n")


def menu():
    while True:

        try:
            choose = int(
                input("\n1.\tGeneration pair (secret,public) keys.\n2.\tSignature.\n3.\tExit.\n-\t"))
        except Exception:
            print("Input error. Try again!")
            continue
        else:
            if choose == 1:  # generation keys
                gen_keys()
            elif choose == 2:  # encryption
                signature()
            elif choose == 3:  # exit
                break
            else:
                print(f"Incorrect input.")
                continue


menu()


# msg.txt
# results/PubKey - 2022-04-30 15-53-24.json
# results/SecKey - 2022-04-30 15-53-24.json
