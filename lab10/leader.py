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
from gen_param import RsaKeys

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



def p_q_generating():
    flag = True
    q = 0
    k = 0
    prime_mod = 0
    while flag:
        prime_mod = RsaKeys().prime_num(1024)
        time_mark = time.time()
        for maybe_q in primerange(547, (prime_mod - 1) // 2):
            if round(time.time() - time_mark) > 1:
                break
            if (prime_mod - 1) % maybe_q == 0:
                q = maybe_q
                k = (prime_mod - 1) // q
                flag = False
                break
    return prime_mod, q, k


def int_to_bytes(num: int) -> bytes:
    return num.to_bytes(ceil(log2(num) / 8), "big")



msg = "Hello, World!".encode()
send_data = {}
# users = {"user_1": {"ip": "localhost", "port": 50500}, "user_2": {"ip": "localhost", "port": 50555}}
users = {"user_1": {"ip": "localhost", "port": 50500}}
print(f"Users:\t{users}")

prime_p, prime_q, k = p_q_generating()
parent = RsaKeys().gen_parent_element(prime_p)
n_mod, public_exp, secret_d = RsaKeys().under_group_params(512)
alpha = pow(parent, k, prime_p)
z_param = RsaKeys().prime_num(1024)
print(f"p - {prime_p}")
print(f"q - {prime_q} || k = {k}")

print(f"Parent - {parent}")
print(f"Alpha - {alpha}")

for user_name in users:
    send_data[user_name] = {"mark": "first", "prime_p": prime_p, "prime_q": prime_q, "alpha": alpha}

# user_pub_res = client(users, send_data)
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
print(send_data)
# r_param_res = client(users, send_data)
r_param_res = client_decor(users, send_data)

leader_t = random.randint(2, prime_q-1)

leader_r_param = pow(alpha, leader_t, prime_p)
R_universe = leader_r_param
for user_name in users:
    users[user_name]["R"] = r_param_res[user_name]
    R_universe *= users[user_name]["R"]

R_universe %= prime_p


E_param = GOST_R_34_12_2012.GOST_34_11_2012(msg + int_to_bytes(R_universe) + int_to_bytes(universe), 512).hash_()

E_param = int.from_bytes(E_param, "big")

print(f"E - {E_param}")

for user_name in users:
    send_data[user_name] = {"mark": "three", "E": E_param}

s_param_res = client_decor(users, send_data)
S_universe = 0
lead_s = leader_t + pow((E_param * z_param), 1, prime_q)
S_universe = lead_s
print(f"S lead - {S_universe}")
for user_name in users:
    users[user_name]["S"] = s_param_res[user_name]
    print(f"users - {users}")
    my_pow = pow(users[user_name]["lambda"] * E_param * -1, 1, prime_q)
    step_one = pow(users[user_name]["public"], my_pow, prime_p)  # users[user_name]["R"] ==
    step_two = pow(alpha, users[user_name]["S"], prime_p)
    finally_step = (step_one * step_two) % prime_p

    if users[user_name]["R"] == finally_step:
        print("!!!!!!!!!Right!!!!!!!!!!!!!")
        S_universe += users[user_name]["S"]
        print(S_universe)

S_universe %= prime_q

sign = {"U": universe, "E": E_param, "S": S_universe}

print(sign)

L_key = pow(alpha, z_param, prime_p)

mp_pow = pow((-1)*E_param, 1, prime_q)

step_one = pow(universe * L_key, mp_pow, prime_p)
step_two = pow(alpha, S_universe, prime_p)
R_under = (step_one * step_two) % prime_p
E_under = GOST_R_34_12_2012.GOST_34_11_2012(msg + int_to_bytes(R_under) + int_to_bytes(universe), 512).hash_()
E_under = int.from_bytes(E_under, "big")
print(E_under == E_param)
print(R_under == R_universe)


# with open("file_test.json") as f:
#     client(json.load(f), users)
