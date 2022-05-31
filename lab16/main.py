import logging
import random
import os
import art
import socket
import json
from datetime import datetime
from myScripts.gost_stribog import gost_256_512
from myScripts.sha_ import sha_256_512
from myScripts.my_rsa import prime_num, alg_euc, RSA
from myScripts.text_tags import Tag
from myScripts.signature import gen_signature
import math
import timeit

lab_name = os.path.basename(os.getcwd())

my_name = "Alice"
my_user_id = 4932

users = {"Bob": 2605}


def welcome():
    art.tprint(lab_name, font="chiseled")
    print(f"{Tag.blue} Host Id: {my_user_id}")
    print(f"{Tag.blue} Host Name: {my_name}\n")


def fragmentation(data_to_send):
    if type(data_to_send) is dict:
        return [json.dumps(data_to_send).encode()[x:x + 1024] for x in
                range(0, len(json.dumps(data_to_send).encode()), 1024)]
    elif type(data_to_send) is bytes:
        return [data_to_send[x:x + 1024] for x in
                range(0, len(data_to_send), 1024)]


def client(data_to_send: dict or bytes):
    result = b""
    package_blocks = fragmentation(data_to_send)

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(("localhost", 50544))

    for block in package_blocks:
        client_sock.sendall(block)
        data = client_sock.recv(1024)
        if data.decode() == str(len(package_blocks) - 1):
            client_sock.sendall(b"DataPut")
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                result += data
    client_sock.close()

    return result


def new_signature(recipient_id: int, session_key_: bytes, time_mark_: str):
    body_signature = {"RecipientId": recipient_id, "SessionKey": session_key_.hex(), "TimeMark": time_mark_}
    body_signature = json.dumps(body_signature).encode()
    pub_signature_key = json.load(open("source/signatureKeys/public_key.json", "r", encoding='utf-8'))
    sec_signature_key = json.load(open("source/signatureKeys/privat_key.json", "r", encoding='utf-8'))
    signature_ = gen_signature(body_signature, sha_256_512, pub_key=pub_signature_key, sec_key=sec_signature_key)
    return signature_


welcome()

session_key = prime_num(256).to_bytes(32, "big")
print(f"{Tag.blue} Session key generated: {session_key.hex()}")

time_mark = str(datetime.now())[2:-7].replace(" ", "-").replace(":", "-")
print(f"{Tag.blue} Time mark generated: {time_mark}")

recipient_ID = users["Bob"]
signature = new_signature(recipient_id=recipient_ID, session_key_=session_key, time_mark_=time_mark)

body_encrypt = {"SessionKey": session_key.hex(), "TimeMark": time_mark, "Signature": signature}
body_encrypt = json.dumps(body_encrypt).encode()

pub_encrypt_key = json.load(open("source/encryptionKeys/public_key.json", "r", encoding='utf-8'))
sec_encrypt_key = json.load(open("source/encryptionKeys/privat_key.json", "r", encoding='utf-8'))

encrypted_session_key = RSA().encrypt(pub_encrypt_key, body_encrypt)

print(f"{Tag.blue} Session key encrypted: {encrypted_session_key.hex()}")

letter = {"EncryptedSessionKey": encrypted_session_key.hex()}
print(f'{Tag.blue} Session key sent.')
answer = client(letter)
print(f'{Tag.blue} Session key received.')
if answer == b"Correct":
    print(f'{Tag.green} Session key is correct.')
elif answer == b"Incorrect":
    print(f'{Tag.red} Session key is incorrect.')
else:
    print(f'{Tag.red} Session key is not received: {answer}.')


