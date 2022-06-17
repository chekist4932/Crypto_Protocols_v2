import json
import pprint
import random
from my_rsa import prime_num
from client import client
import os
import art
from text_tags import Tag

my_name = "Leader"
users = {
    "Alice": {"R": 0, "Port": 50444},
    "Bob": {"R": 0, "Port": 50555}
}
prime_ = prime_num(1024)
n = len(users)
print(f"N : {n}")
users["Alice"]["R"] = random.randint(1, prime_-1)
users["Bob"]["R"] = random.randint(1, prime_-1)

print(f"P : {prime_}")
print(f"r0 : {users['Alice']['R']}")
print(f"r1 : {users['Bob']['R']}")
deg_polynomial = 2 * n


def welcome():
    lab_name = os.path.basename(os.getcwd())
    art.tprint(lab_name, font="chiseled")
    print(f"{Tag.blue} Host Name: {my_name}\n")


def client_decor():
    for username in users:
        client(users[username], users[username]["Port"])


def gen_polynomial():
    polynomial_ = [[random.randint(1, prime_ - 1) for _ in range(deg_polynomial)] for _ in range(deg_polynomial)]

    for i in range(deg_polynomial):
        for j in range(deg_polynomial):
            polynomial_[j][i] = polynomial_[i][j]

    return polynomial_


def gen_user_polynomial(polynomial_: list, temp_r0: int):
    user_polynomial = []
    for i in range(deg_polynomial):
        temp = 0
        for j in range(deg_polynomial):
            temp += polynomial_[j][i] * pow(temp_r0, i)
        user_polynomial.append(temp % prime_)
    return user_polynomial


welcome()

polynomial = gen_polynomial()

pprint.pprint(polynomial)

for user_name in users:
    users[user_name]['g(X)'] = gen_user_polynomial(polynomial, users[user_name]["R"])
    users[user_name]['OtherR'] = users["Bob"]["R"] if user_name == "Alice" else users["Alice"]["R"]
    users[user_name]['DegPolynomial'] = deg_polynomial
    users[user_name]['Prime'] = prime_

client_decor()
