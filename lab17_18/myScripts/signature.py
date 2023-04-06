# Меню лабораторной работы №3. "Реализация RSA согласно стандартов PKCS 7, PKCS 8, PKCS 12".
import json
import logging
from datetime import datetime

from myScripts.my_rsa import RSA
from myScripts.text_tags import Tag


def check(set_of_attr: dict):
    user_sign = set_of_attr["UserSignature"]
    tms = json.dumps(set_of_attr["Timestamp"]).encode()

    enc_center_signature = set_of_attr["CenterSignature"]

    center_pub_key = {"N": set_of_attr["CenterSubjectPublicKeyInfo"]["SubjectPublicKeyInfo"]["N"],
                      "publicExponent": set_of_attr["CenterSubjectPublicKeyInfo"]["SubjectPublicKeyInfo"][
                          "publicExponent"]
                      }

    decrypt_center_signature = RSA().decrypt(center_pub_key, bytes.fromhex(enc_center_signature), mode=1)

    if decrypt_center_signature.hex() == (user_sign + tms.hex()):
        return True
    else:
        return False


def gen_signature(msg: bytes, hash_, pub_key: dict, sec_key: dict, size_: int = 256):
    try:
        hash_msg, hash_name = hash_(msg, size_, mode=1)
        hash_type = hash_name + str(size_)
    except Exception:
        logging.exception("HashError")
        raise ValueError("Incorrect hash object")
    print(f"{Tag.blue} Signature in progress.")
    try:
        user_signature = RSA().encrypt(sec_key, hash_msg, mode=1)
    except ValueError:
        logging.exception("SignatureError")

    else:
        time_mark = str(datetime.now())[2:-7].replace(" ", "-").replace(":", "-")
        sign_dict = RSA().PKCS_7_CAdES(msg.hex(), user_signature.hex(),
                                       hash_type, pub_key, time_mark)

        return sign_dict
        # input(f"{Tag.pink} Enter for send to Time Stamp Center\n-\t")
        #
        # with open(f"results\\Signature {time_mark}.json", "r", encoding="utf-8") as jf:
        #     sign_dict = json.load(jf)

        # res_time_center = client(sign_dict)
        # if res_time_center == b"":
        #     return "ERROR in TimeStampCentre"
        # else:
        #
        #     set_of_attr = json.loads(res_time_center.decode())
        #
        #     if check(set_of_attr):
        #         res_dict = json.load(open(f"results\\Signature {time_mark}.json", "r", encoding="utf-8"))
        #
        #         res_dict["SignerInfos"]["UnsignedAttributes"][
        #             "SET OF AttributeValue"] = set_of_attr
        #
        #         json.dump(res_dict, open(f"results\\Signature {time_mark}.json", "w", encoding="utf-8"), indent=4)
        #
        #         return res_dict
