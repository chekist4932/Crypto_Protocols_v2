import random
import json
import socket
from source.gost_stribog import gost_256_512
from source.my_rsa import RSA

my_name = "Alice"
user_id = 4932
users = {"Bob": 2605}
insertion_tag = "\033[36m[+]\033[0m"
key = {"key": "", "nonce": ""}




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


def gen_rand_numb():
    return random.randint(10000000, 99999999)


with open("public_key.json", "r", encoding="utf-8") as file:
    public_key = json.load(file)

print(f"Public: {public_key}")

rand_num_z = gen_rand_numb()
# print(rand_num_z)
hash_rand_num_z = gost_256_512(json.dumps(rand_num_z).encode(), 512)

argument_encrypt = {"RandomParam": rand_num_z, "Id": user_id}



encrypted_data = RSA.encrypt(pub_key=public_key, bytes_mess=json.dumps(argument_encrypt).encode())

letter = {"Hash": hash_rand_num_z, "Argument": encrypted_data.hex()}
print(f"{insertion_tag} Random number z: {rand_num_z}")
print(f"{insertion_tag} Data sent to: {users}")
bob_answer = client(letter)
print(f"{insertion_tag} Answer from: {users}")
# print(bob_answer)
try:
    if json.loads(bob_answer.decode()) == rand_num_z:
        print(f"{insertion_tag} Number: {json.loads(bob_answer.decode())}")
        print(f"{insertion_tag} Authentication passed.")
except Exception:
    print(f"{insertion_tag} Authentication failed.")
