import datetime
import random
import json
import socket
from Crypto.Cipher import AES


my_name = "Alice"

users = {"Bob": 2605}

user_id = 4932


def client(send_file: dict):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(("localhost", 50500))
    res = b""
    dd = [json.dumps(send_file).encode()[x:x + 1024] for x in range(0, len(json.dumps(send_file).encode()), 1024)]
    for i in dd:
        client_sock.sendall(i)
        data = client_sock.recv(1024)

        if data.decode() == str(len(dd) - 1):
            client_sock.sendall(b"DataPut")
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                res += data

    client_sock.close()
    # print(res)
    if res == b"Error" or res == b"InDa" or res == b"ErrorEx":
        res = False
    return res


def gen_key():
    return (random.randint(2 ** 127, 2 ** 128)).to_bytes(16, "big")


def gen_random_numb():
    return random.randint(10000000, 99999999)


def gen_random_timestamp():
    hour = str(random.randint(0, 23)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    second = str(random.randint(0, 59)).zfill(2)
    return f"{hour}:{minute}:{second}"

def get_message():
    while True:
        try:
            first_message = input("Input first message:\t")
            second_message = input("Input second message:\t")
        except Exception:
            print("Input error.")
        else:
            return first_message, second_message

def get_rand_param():
    while True:
        choose = input("[+] Choose:\n1. Random number.\n2. Random TimeStamp.\n")
        if choose == "1":
            return gen_random_numb()
        elif choose == "2":
            return gen_random_timestamp()
        else:
            print("Input incorrect. Again.")

first_message, second_message = get_message()

rand_param = get_rand_param()








key = {"key": gen_key().hex()}

cipher = AES.new(bytes.fromhex(key["key"]), AES.MODE_EAX)
nonce = cipher.nonce

key["Nonce"] = nonce.hex()


# print(f"key -- {key}")
client(key)
passport = {"Random param": rand_param, "Id": user_id, "Message1": first_message}
data_to_encrypt = json.dumps(passport).encode()

encrypted_text = cipher.encrypt(data_to_encrypt)

letter = {"Message2": second_message, "E(k)": encrypted_text.hex()}
answer = json.loads(client(letter).decode())
# print(answer)
if answer is not False:
    new_nonce = bytes.fromhex(answer["Nonce"])
    E_k = bytes.fromhex(answer["E(k)"])
    # print(E_k)
    key_ = bytes.fromhex(key["key"])
    try:
        decrypted_data = json.loads(AES.new(key_, AES.MODE_EAX, nonce=new_nonce).decrypt(E_k).decode())
        # print(decrypted_data)
        if decrypted_data["Id"] in users.values() and rand_param == decrypted_data['Random param']:
            print(f"[+] Authentication successful.")
            flag = True
        else:
            print(f"[+] Authentication failed.")
            flag = False
    except Exception:
        flag = False
    else:
        if flag:
            for key_word, val in users.items():
                if val == decrypted_data["Id"]:
                    user_name = key_word
                    break

            print(f"[+] Connected with {user_name}")
            print(f"[+] {user_name}: {decrypted_data['Message3']}")
            print(f"[+] {user_name}: {answer['Message4']}")

else:
    print(f"[+] Authentication failed.")