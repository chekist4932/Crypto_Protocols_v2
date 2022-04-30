import socket
import json
import time
from datetime import datetime

import Fiat
import GOST_R_34_12_2012

import sha_256_512


def load_pkcs(user_sign: bytes, center_sec_key, center_pub_key, hash_type: str):
    utc = str(datetime.utcnow())[2:-7].replace("-", "-").replace(" ", "-").replace(":", "-")
    now = str(datetime.now())[2:-7].replace("-", "-").replace(" ", "-").replace(":", "-")
    timestamp = {"UTCTime": utc, "GeneralizedTime": now}
    tms: bytes = json.dumps(timestamp).encode()

    center_signature: dict = Fiat.Shamir().signature(center_sec_key, user_sign + tms, hash_type)

    set_of_AttributeValue = {"UserSignature": user_sign.hex(),
                             "Timestamp": timestamp,
                             "CenterSignature": center_signature,
                             "CenterSubjectPublicKeyInfo": {
                                 "SubjectPublicKeyInfo": {"publicExponent": center_pub_key["publicExponent"],
                                                          "N": center_pub_key["N"]},
                                 "PKCS10CertRequest": "NULL", "Certificate": "NULL", "PKCS7CertChain-PKCS": "NULL"}
                             }
    with open(f"sends/SetOfAttr-{now}.json", "w", encoding="utf-8") as f:
        json.dump(set_of_AttributeValue, f, indent=4)

    return set_of_AttributeValue


def get_keys(type: str, dict_for_check):
    if type == "FiatSHAMIRdsi":
        directory = "FiatShamir_keys"
        user_pub_key = dict_for_check["CertificateSet"]["SubjectPublicKeyInfo"]
        pub_key = Fiat.Shamir().read_out_file(f"keys/{directory}/PubKey_.json", "pb")
        sek_key = Fiat.Shamir().read_out_file(f"keys/{directory}/SecKey_.json", "sk")
    else:
        raise ValueError("Incorrect type")

    return pub_key, sek_key, user_pub_key


def hashing(msg: bytes, hash_type: str):
    if hash_type == "sha256":
        hash_for_check = sha_256_512.__sha_256(msg)
    elif hash_type == "sha512":
        hash_for_check = sha_256_512.__sha_512(msg)
    elif hash_type == "GOST256":
        hash_for_check = GOST_R_34_12_2012.GOST_34_11_2012(msg, 256).hash_()
    elif hash_type == "GOST512":
        hash_for_check = GOST_R_34_12_2012.GOST_34_11_2012(msg, 512).hash_()
    else:
        raise ValueError("Incorrect hash type")

    return hash_for_check



with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("localhost", 50500))
    # 10.0.126.164
    print(serv_sock)
    serv_sock.listen(4)

    while True:
        # Бесконечно обрабатываем входящие подключения
        client_sock, client_addr = serv_sock.accept()
        print('Connected by', client_addr)
        res = b""
        count = 0
        while True:
            # Пока клиент не отключился, читаем передаваемые
            # им данные и отправляем их обратно
            data = client_sock.recv(1024)
            # print(data)
            if data == b"Data sent":
                dict_for_check = json.loads(res.decode())
                if list(dict_for_check)[0] == "CMSVersion":
                    try:
                        user_type_of_encrypt = dict_for_check["SignerInfos"][
                            "SignatureAlgorithmIdentifier"] # Алгоритм подписи
                        if user_type_of_encrypt == "FiatSHAMIRdsi":
                            user_msg = bytes.fromhex(dict_for_check["EncapsulatedContentInfo"]["OCTET STRING"])
                            # Исходное сообщение
                            user_signature = dict_for_check["SignerInfos"]["SignatureValue"]  # Подпись
                            _hash_type = dict_for_check["SignerInfos"]["DigestAlgorithmIdentifier"]  # Хеш

                            center_pub_key, center_sek_key, user_pub_key = get_keys(user_type_of_encrypt,
                                                                                                dict_for_check)

                            check_flag = Fiat.Shamir().check_signature(user_pub_key, user_signature, user_msg, _hash_type)
                            print("+")
                    except Exception as err:
                        print(err)
                        client_sock.sendall(b"ErrorEx")
                    else:
                        # print("10")
                        if check_flag == True:
                            hash_of_user_sign = hashing(user_msg + json.dumps(user_signature).encode(),
                                                        _hash_type)
                            SetOfAttr = load_pkcs(hash_of_user_sign, center_sek_key, center_pub_key, _hash_type)

                            print(f"SetOfAttribute sent to {client_addr}")
                            client_sock.sendall(json.dumps(SetOfAttr).encode())
                        elif check_flag == False:
                            client_sock.sendall(b"InDa")

                else:
                    client_sock.sendall(b"Error")
                break
            res += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"Close connection with {client_addr}")
        client_sock.close()
