import logging
import random
import json
import socket
import os
import art
from myScripts.gost_stribog import gost_256_512
from myScripts.sha_ import sha_256_512
from myScripts.my_rsa import RSA
from myScripts.text_tags import Tag

my_name = "Bob"
my_user_id = 2605
users = {"Alice": 4932}
insertion_tag = "\033[36m[+]\033[0m"
lab_name = os.path.basename(os.getcwd())

sec_encrypt_key = json.load(open("source/encryptionKeys/privat_key.json", "r", encoding='utf-8'))


def welcome():
    art.tprint(lab_name, font="chiseled")
    print(f"{Tag.blue} Host Id: {my_user_id}")
    print(f"{Tag.blue} Host Name: {my_name}\n")


welcome()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("localhost", 50544))
    # 10.0.126.164
    print(f"{Tag.blue} Socket info: {serv_sock}")
    serv_sock.listen(1)

    while True:
        # Бесконечно обрабатываем входящие подключения
        client_sock, client_addr = serv_sock.accept()
        print(f'{Tag.blue} Connected with: {client_addr}.')
        result = b""
        count = 0
        while True:
            # Пока клиент не отключился, читаем передаваемые
            # им данные и отправляем их обратно
            data = client_sock.recv(1024)
            # print(data)

            if data == b"DataPut":
                try:
                    letter = json.loads(result.decode())
                    assert type(letter) is dict
                    if "EncryptedSessionKey" in letter.keys():
                        print(f'{Tag.blue} Session key received.')
                        encrypted_session_key = bytes.fromhex(letter["EncryptedSessionKey"])
                        decrypted_session_key = RSA().decrypt(sec_encrypt_key, encrypted_session_key)
                        decrypted_session_key = json.loads(decrypted_session_key)
                        print(f"{Tag.blue} Process signature verification.")
                        signature_value = decrypted_session_key["Signature"]["SignerInfos"]["SignatureValue"]
                        public_signature_key = decrypted_session_key["Signature"]["CertificateSet"]

                        hash_into_signature = RSA().decrypt(sec_key=public_signature_key,
                                                            encrypted_msg=bytes.fromhex(signature_value), mode=1)

                        body_signature = {"RecipientId": my_user_id, "SessionKey": decrypted_session_key["SessionKey"],
                                          "TimeMark": decrypted_session_key["TimeMark"]}
                        body_signature = json.dumps(body_signature).encode()

                        body_signature = sha_256_512(body_signature, 256)

                        if body_signature.hex() == hash_into_signature.hex():
                            print(f'{Tag.pink} Session key: {decrypted_session_key["SessionKey"]}.')
                            print(f'{Tag.green} Session key is correct.')
                            client_sock.sendall(b"Correct")
                        else:
                            print(f'{Tag.pink} Session key: {decrypted_session_key["SessionKey"]}.')
                            print(f'{Tag.red} Session key is incorrect.')
                            client_sock.sendall(b"Incorrect")

                except Exception as err:
                    logging.exception("DataError")
                    print(f'{Tag.red} {err}')
                    client_sock.sendall(b"DataError")

                break
            result += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"{Tag.blue} Close connection with: {client_addr}.\n")
        client_sock.close()
