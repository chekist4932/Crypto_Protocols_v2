import socket
import json
import time
from datetime import datetime
import GOST_R_34_12_2012
import my_rsa
import sha_256_512


def load_pkcs(user_sign, center_sec_key, center_pub_key):
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
    with open(f"sends/SetOfAttr-{now}.json", "w", encoding="utf-8") as f:
        json.dump(set_of_AttributeValue, f, indent=4)

    return set_of_AttributeValue


def get_keys(type: str):
    if type == "RSAdsi":
        directory = "rsa_keys"
    else:
        raise ValueError("Incorrect type")

    pub_key = my_rsa.RSA().read_out_file(f"keys/{directory}/PubKey_.json", "pb")
    sek_key = my_rsa.RSA().read_out_file(f"keys/{directory}/SecKey_.json", "sc")
    return pub_key, sek_key


def hashing(msg, hash_type: str):
    if hash_type == "sha256":
        hash_for_check = sha_256_512.__sha_256(bytes.fromhex(msg))
    elif hash_type == "sha512":
        hash_for_check = sha_256_512.__sha_512(bytes.fromhex(msg))
    elif hash_type == "GOST256":
        hash_for_check = GOST_R_34_12_2012.GOST_34_11_2012(bytes.fromhex(msg), 256).hash_()
    elif hash_type == "GOST512":
        hash_for_check = GOST_R_34_12_2012.GOST_34_11_2012(bytes.fromhex(msg), 512).hash_()
    else:
        raise ValueError("Incorrect hash type")

    return hash_for_check


def check(msg, hash_type, pub_k, encrypt_signature):
    decrypt_signature = my_rsa.RSA().decrypt(pub_k, bytes.fromhex(encrypt_signature))
    hash_for_check = hashing(msg, hash_type)
    # print(hash_for_check)
    # print(decrypt_signature)
    if hash_for_check == decrypt_signature:
        return True
    else:
        return False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("10.0.147.102", 54678))
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
            if data == b"Data sent":
                dict_for_check = json.loads(res.decode())
                if list(dict_for_check)[0] == "CMSVersion":  # Подпись
                    try:
                        user_msg = dict_for_check["EncapsulatedContentInfo"]["OCTET STRING"]
                        user_signature = dict_for_check["SignerInfos"]["SignatureValue"]
                        user_hash_type = dict_for_check["SignerInfos"]["DigestAlgorithmIdentifier"]
                        user_type_of_encrypt = dict_for_check["SignerInfos"]["SignatureAlgorithmIdentifier"]
                        user_pub_key = dict_for_check["CertificateSet"]["SubjectPublicKeyInfo"]["publicExponent"]
                        user_mod_n = dict_for_check["CertificateSet"]["SubjectPublicKeyInfo"]["N"]
                        center_pub_key, center_sek_key = get_keys(user_type_of_encrypt)
                        check_flag = check(user_msg, user_hash_type, [user_mod_n, user_pub_key], user_signature)

                    except Exception as err:
                        client_sock.sendall(b"Error")
                    else:
                        # print("10")
                        if check_flag == True:
                            ref_user_signature = hashing(user_msg + user_signature, user_hash_type)
                            SetOfAttr = load_pkcs(ref_user_signature, center_sek_key, center_pub_key)
                            print(f"End with {client_addr}")
                            client_sock.sendall(json.dumps(SetOfAttr).encode())
                        elif check_flag == False:
                            client_sock.sendall(b"InDa")

                else:
                    client_sock.sendall(b"Error")
                break
            res += data
            client_sock.sendall(str(count).encode())
            count += 1

        client_sock.close()
