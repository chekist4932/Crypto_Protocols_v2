import json
import pprint
import random
from my_rsa import prime_num, gen_inverse_modulo
from client import client
import os
import art
from text_tags import Tag

my_name = "Leader"


# deg_polynomial = 2 if n <= 2 else random.randint(3, n)


def welcome():
    lab_name = os.path.basename(os.getcwd())
    art.tprint(lab_name, font="chiseled")
    print(f"{Tag.blue} Host Name: {my_name}\n")


def gen_polynomial(prime_, deg_polynomial):
    polynomial_ = [random.randint(1, prime_ - 1) for _ in range(deg_polynomial + 1)]
    return polynomial_


def func_at_x(poly: list, x: int, deg_polynomial):
    result = poly[0]
    for i in range(1, deg_polynomial + 1):
        result += (poly[i] * pow(x, i))
    return result


def gen_c_param(users_r_: list, prime_: int):
    c_params = []
    for i in range(len(users_r_)):
        temp_c = 1
        for j in range(len(users_r_)):
            if i != j:
                temp_c = temp_c * (users_r_[j] * gen_inverse_modulo(prime_, (users_r_[j] - users_r_[i]) % prime_))

        c_params.append(temp_c)
    # print(f"Ci: {c_params}")
    return c_params


# welcome()
def work():
    prime_ = prime_num(512)
    n = 4
    deg_polynomial = 3
    # print(prime_)
    polynomial = gen_polynomial(prime_, deg_polynomial)
    # print(f"Polynomial: {polynomial}")
    users_r = []
    while len(users_r) < n:
        r = random.randint(2, prime_ - 1)
        if r not in users_r:
            users_r.append(r)
    print(f"Poly: {polynomial}")
    print(f'R:    {users_r}')

    users_c = gen_c_param(users_r, prime_)

    s = polynomial[0]

    new_s = 0
    for i in range(len(users_r)):
        new_s += (func_at_x(polynomial, x=users_r[i], deg_polynomial=deg_polynomial) * users_c[i])

    print(f'S : {s}')
    print(f'S~: {round(new_s % prime_)}\n')

    if round(new_s % prime_) == s:
        return True


# checker = 0
# for i in range(100):
#     if work():
#         checker += 1
# print(checker)
print(work())