import random
import json
import socket
from Crypto.Cipher import AES

my_name = "Alice"
user_id = 4932
users = {"Bob": 2605}
insertion_tag = "\033[36m[+]\033[0m"
key = {"key": "", "nonce": ""}
user_name = ""
rand_B = 0


def client(data_to_send: dict):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(("localhost", 50544))
    result = b""
    package_blocks = [json.dumps(data_to_send).encode()[x:x + 1024] for x in
                      range(0, len(json.dumps(data_to_send).encode()), 1024)]
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


def gen_key():
    return (random.randint(2 ** 127, 2 ** 128)).to_bytes(16, "big")


def gen_rand_numb():
    return random.randint(10000000, 99999999)


def get_message():
    while True:
        try:
            message = input(f"{insertion_tag} Input message:\t")
        except Exception:
            print(f"{insertion_tag} Input error.")
        else:
            return message



key['key'] = gen_key().hex()
client(data_to_send=key)

first_message = get_message()
rand_A = gen_rand_numb()
first_letter = {"Random_A": rand_A, "Message1": first_message}
first_answer = client(data_to_send=first_letter)
flag = False

try:
    first_answer = json.loads(first_answer.decode())
    if "E(k)" in first_answer.keys():
        encrypted_data = bytes.fromhex(first_answer["E(k)"])
        nonce = bytes.fromhex(first_answer["nonce"])
        key_ = bytes.fromhex(key['key'])
        decrypted_data = json.loads(AES.new(key_, AES.MODE_EAX, nonce=nonce).decrypt(encrypted_data).decode())
        if decrypted_data["Id"] in users.values():
            for key_word, val in users.items():
                if val == decrypted_data["Id"]:
                    user_name = key_word
                    break
            if decrypted_data['Random_A'] == rand_A:
                rand_B = decrypted_data['Random_B']
                print(f"{insertion_tag} Authentication passed.")
                print(f"{user_name}: {decrypted_data['Message2']}")
                print(f"{user_name}: {first_answer['Message3']}")
                flag = True
            else:
                print(f"{insertion_tag} Authentication failed.")
except Exception as error:
    print(f"{insertion_tag} Authentication failed: {error}")


if flag:
    fourth_message = get_message()
    encrypt_argument = {
        'Random_B': rand_B,
        'Random_A': rand_A,
        'Id': user_id,
        'Message4': fourth_message
    }
    data_to_encrypt = json.dumps(encrypt_argument).encode()
    cipher = AES.new(bytes.fromhex(key["key"]), AES.MODE_EAX)
    nonce = cipher.nonce
    encrypted_text: bytes = cipher.encrypt(data_to_encrypt)
    third_letter = {"Message5": get_message(),
                    "E(k)": encrypted_text.hex(),
                    'nonce': nonce.hex()}
    answer = client(data_to_send=third_letter)

    if answer == b"Authentication passed":
        print(f'{insertion_tag} Authentication completed.')