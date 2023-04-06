import socket
import json
from math import ceil, log2
from datetime import datetime

import GOST_R_34_12_2012
import my_rsa
import sha_256_512


def get_center_signature(user_sign: bytes, center_pub_key: list, center_sec_key: list):
    pub_key = {"SubjectPublicKeyInfo": {"publicExponent": center_pub_key[1], "N": center_pub_key[0]},
               "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"}

    utc = str(datetime.utcnow())[2:-7].replace("-", "-").replace(" ", "-").replace(":", "-")
    now = str(datetime.now())[2:-7].replace("-", "-").replace(" ", "-").replace(":", "-")
    timestamp = {"UTCTime": utc, "GeneralizedTime": now}
    tms = json.dumps(timestamp).encode()
    center_signature = my_rsa.RSA().encrypt(center_sec_key, user_sign + tms).hex()
    set_of_AttributeValue = {"UserSignature": user_sign.hex(),
                             "Timestamp": timestamp,
                             "CenterSignature": center_signature,
                             "CenterSubjectPublicKeyInfo": pub_key
                             }
    with open(f"sends/SetOfAttr-{now}.json", "w", encoding="utf-8") as file:
        json.dump(set_of_AttributeValue, file, indent=4)

    return set_of_AttributeValue


def get_keys():
    directory = "rsa_keys"
    pub_key: list = my_rsa.RSA().read_out_file(f"keys/{directory}/PubKey_.json", "pb")
    sek_key: list = my_rsa.RSA().read_out_file(f"keys/{directory}/SecKey_.json", "sc")
    return pub_key, sek_key


def int_to_bytes(num: int) -> bytes:
    return num.to_bytes(ceil(log2(num) / 8), "big")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("localhost", 50228))
    print(serv_sock)
    serv_sock.listen(4)

    while True:
        # Бесконечно обрабатываем входящие подключения
        client_sock, client_addr = serv_sock.accept()
        print('\n[+] Connected to', client_addr)
        res = b""
        count = 0
        while True:
            data = client_sock.recv(1024)
            if data == b"Data sent":
                try:
                    signature_ = json.loads(res.decode())
                    hash_type = signature_["DigestAlgorithmIdentifiers"]
                    msg = signature_["EncapsulatedContentInfo"]["OCTET STRING"]
                    E_param = signature_["SignerInfos"]["SignatureValue"]["E"]
                    universe = signature_["SignerInfos"]["SignatureValue"]["U"]
                    S_universe = signature_["SignerInfos"]["SignatureValue"]["S"]
                    user_signature = signature_["SignerInfos"]["SignatureValue"]

                    L_key = signature_["CertificateSet"]["SubjectPublicKeyInfo"]["publicExponent"]
                    prime_p = signature_["CertificateSet"]["SubjectPublicKeyInfo"]["prime_p"]
                    prime_q = signature_["CertificateSet"]["SubjectPublicKeyInfo"]["prime_q"]
                    alpha = signature_["CertificateSet"]["SubjectPublicKeyInfo"]["alpha"]

                    mp_pow = pow((-1) * E_param, 1, prime_q)
                    step_one = pow(universe * L_key, mp_pow, prime_p)
                    step_two = pow(alpha, S_universe, prime_p)
                    R_under = (step_one * step_two) % prime_p
                    E_under = GOST_R_34_12_2012.GOST_34_11_2012(msg.encode() + int_to_bytes(R_under) + int_to_bytes(universe),
                                                                512).hash_()
                    E_under = int.from_bytes(E_under, "big")
                except Exception as err:
                    print(f"[+] {err}")
                    client_sock.sendall(b"IncorrectData")
                else:
                    if E_under == E_param:
                        print("[+] Signature is correct.")
                        centre_public_key, centre_secret_key = get_keys()
                        print(f"[+] 'Set Of Attribute Value' sent to {client_addr}")
                        SetOfAttr = get_center_signature(json.dumps(user_signature).encode(), centre_public_key,
                                                         centre_secret_key)
                        client_sock.sendall(json.dumps(SetOfAttr).encode())
                    else:
                        print("[+] Signature incorrect.")
                        client_sock.sendall(b"IncorrectSignature")

                break
            res += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"[+] Close connection with {client_addr}")
        client_sock.close()
