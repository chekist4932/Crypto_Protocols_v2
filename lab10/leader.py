# PKCS 7
import random
import socket
import json

import sympy
from sympy import isprime, primerange
import time
from datetime import datetime
from math import ceil, log2

import GOST_R_34_12_2012
import client_TimeStampCentre
import my_rsa
from gen_param import under_group_params, prime_num, gen_parent_element, generation_prime_p_and_prime_q

insertion = "\033[36m[+]\033[0m"
users = {"user_1": {"ip": "localhost", "port": 50500}, "user_2": {"ip": "localhost", "port": 50555}}
hash_type = "GOST512"


def client_decor(users: dict, send_file: dict):
    answers_dict = {}
    for user_name in users:
        answers_dict[user_name] = client_2(users[user_name], send_file[user_name])["answer"]
    return answers_dict


def client_2(user: dict, send_file: dict):
    answers_dict = {}
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((user["ip"], user["port"]))

    answer = b""
    dd = [json.dumps(send_file).encode()[x:x + 1024] for x in
          range(0, len(json.dumps(send_file).encode()), 1024)]

    for i in dd:
        client_sock.sendall(i)
        data = client_sock.recv(1024)
        # print(data)
        if data.decode() == str(len(dd) - 1):
            client_sock.sendall(b"data put")
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                answer += data

    client_sock.close()
    # print(answer)
    if answer == b"Error" or answer == b"InDa" or answer == b"ErrorEx":
        answers_dict["answer"] = False
    else:
        answers_dict["answer"] = json.loads(answer.decode())
    return answers_dict


def int_to_bytes(num: int) -> bytes:
    return num.to_bytes(ceil(log2(num) / 8), "big")


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


def path_getter():
    while True:
        try:
            path = input(f"{insertion} Input path to message: ")
            file = open(path)
        except Exception as err:
            print(f"{insertion} Incorrect path. {err}.")
            continue
        else:
            file.close()
            return path


def open_file() -> bytes:
    while True:
        path = path_getter()
        try:
            msg = open(path, "r", encoding="utf-8").read().encode("utf-8")
        except Exception as err:
            print(f"{insertion} Input error. Try again!. {err}")
            continue
        else:
            return msg

msg = open_file()

print(f"{insertion} Process started.")

# msg = "Hello, World!".encode()

send_data = {}

prime_p, prime_q, k = generation_prime_p_and_prime_q()
parent = gen_parent_element(prime_p)
n_mod, public_exp, secret_d = under_group_params(512)
alpha = pow(parent, k, prime_p)
z_param = prime_num(1024)

print(f"{insertion} Group params generated.")

for user_name in users:
    send_data[user_name] = {"mark": "first", "prime_p": prime_p, "prime_q": prime_q, "alpha": alpha}

user_pub_res = client_decor(users, send_data)

hash_msg = GOST_R_34_12_2012.GOST_34_11_2012(msg, 512).hash_()
int_hash = int.from_bytes(hash_msg, "big")

universe = 1

for user_name in users:
    user_key = user_pub_res[user_name]
    users[user_name]["public"] = user_key
    lambda_ = pow(int_hash + user_key, secret_d, n_mod)
    universe *= pow(user_key, lambda_, prime_p)
    users[user_name]["lambda"] = lambda_
    send_data[user_name] = {"mark": "two", "lambda": lambda_}
universe %= prime_p

r_param_res = client_decor(users, send_data)
leader_t = random.randint(2, prime_q - 1)
leader_r_param = pow(alpha, leader_t, prime_p)
R_universe = leader_r_param
for user_name in users:
    users[user_name]["R"] = r_param_res[user_name]
    R_universe *= users[user_name]["R"]
R_universe %= prime_p

E_param = GOST_R_34_12_2012.GOST_34_11_2012(msg + int_to_bytes(R_universe) + int_to_bytes(universe), 512).hash_()
E_param = int.from_bytes(E_param, "big")

for user_name in users:
    send_data[user_name] = {"mark": "three", "E": E_param}

s_param_res = client_decor(users, send_data)
S_universe = 0
lead_s = leader_t + pow((E_param * z_param), 1, prime_q)
S_universe += lead_s

correct_mark = 0
for user_name in users:
    users[user_name]["S"] = s_param_res[user_name]
    my_pow = pow(users[user_name]["lambda"] * E_param * -1, 1, prime_q)
    step_one = pow(users[user_name]["public"], my_pow, prime_p)
    step_two = pow(alpha, users[user_name]["S"], prime_p)
    finally_step = (step_one * step_two) % prime_p

    if users[user_name]["R"] == finally_step:
        S_universe += users[user_name]["S"]
        correct_mark += 1
S_universe %= prime_q

if correct_mark == len(users):
    print(f"{insertion} Signature created successfully.")

    time_mark = str(datetime.now())[2:-7].replace(" ", "-").replace(":", "-")
    sign = {"U": universe, "E": E_param, "S": S_universe}
    L_key = pow(alpha, z_param, prime_p)
    signature_ = {"CMSVersion": "1",
                  "DigestAlgorithmIdentifiers": hash_type,
                  "EncapsulatedContentInfo": {"ContentType": "text", "OCTET STRING": msg.decode()},
                  "CertificateSet": {
                      "SubjectPublicKeyInfo": {"publicExponent": L_key, "prime_p": prime_p, "prime_q": prime_q,
                                               "alpha": alpha},
                      "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"
                  },
                  "RevocationInfoChoises": "NULL",
                  "SignerInfos":
                      {"CMSVersion": "1",
                       "SignerIdentifier": "Цой Георгий",
                       "DigestAlgorithmIdentifier": hash_type,
                       "SignedAttributes": "NULL",
                       "SignatureAlgorithmIdentifier": "GROUPdsi",
                       "SignatureValue": sign,
                       "UnsignedAttributes":
                           {"OBJECT IDENTIFIER": "signature-time-stamp",
                            "SET OF AttributeValue":
                                " "
                            }
                       }
                  }
    file = open(f"results\\Signature {time_mark}.json", "w", encoding="utf-8")
    json.dump(signature_, file, indent=4)
    file.close()
    file_to_TimeStampCentre = json.load(open(f"results\\Signature {time_mark}.json", "r", encoding="utf-8"))
    input(f"{insertion} Send to the TimeStampCentre. For start press any key.")
    SetOfAttr = json.loads(client_TimeStampCentre.client(file_to_TimeStampCentre).decode())

    if type(SetOfAttr) is dict and check(SetOfAttr):
        file = open(f"results\\Signature {time_mark}.json", "r", encoding="utf-8")
        res_dict = json.load(file)
        file.close()
        file = open(f"results\\Signature {time_mark}.json", "w", encoding="utf-8")
        res_dict["SignerInfos"]["UnsignedAttributes"][
            "SET OF AttributeValue"] = SetOfAttr
        json.dump(res_dict, file, indent=4)
        file.close()
        print(f"{insertion} Timestamp is correct.")
        print(f"{insertion} Hash type:\t{res_dict['DigestAlgorithmIdentifiers']}")
        print(
            f"{insertion} Alg signature:\t{res_dict['SignerInfos']['SignatureAlgorithmIdentifier']}")
        print(f"{insertion} Author signature:\t{res_dict['SignerInfos']['SignerIdentifier']}")
        print(
            f"{insertion} UTCTime:\t{res_dict['SignerInfos']['UnsignedAttributes']['SET OF AttributeValue']['Timestamp']['UTCTime']}")
        print(
            f"{insertion} Time of center:\t{res_dict['SignerInfos']['UnsignedAttributes']['SET OF AttributeValue']['Timestamp']['GeneralizedTime']}")
        print(f"{insertion} Process done.")
    else:
        print(f"{insertion} Error in TimeStampCentre: {SetOfAttr.decode()}")
else:
    print(f"{insertion} Error creating signature.")
