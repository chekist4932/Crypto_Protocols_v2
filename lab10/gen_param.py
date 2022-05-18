import random
import math
import sympy
import time
from datetime import datetime


def generation_prime_p_and_prime_q():
    flag = True
    q = 0
    k = 0
    prime_mod = 0
    while flag:
        prime_mod = prime_num(1024)
        time_mark = time.time()
        for maybe_q in sympy.primerange(547, (prime_mod - 1) // 2):
            if round(time.time() - time_mark) > 1:
                break
            if (prime_mod - 1) % maybe_q == 0:
                q = maybe_q
                k = (prime_mod - 1) // q
                flag = False
                break
    return prime_mod, q, k


def under_group_params(key_digit):
    prime_1 = prime_num(key_digit)
    prime_2 = prime_num(key_digit)
    phi = (prime_1 - 1) * (prime_2 - 1)
    while True:
        exp = random.randint(1, phi - 1)
        mod, a, d = alg_euc(phi, exp)
        if mod ^ 1 == 0 and ((d * exp) % phi) ^ 1 == 0:
            if d < 0:
                d += phi
            break
    return prime_1 * prime_2, exp, d


def gen_parent_element(prime_mod):
    for maybe_parent in range(2, prime_mod):
        if pow(maybe_parent, 2, prime_mod) ^ 1 != 0 and pow(maybe_parent, (prime_mod - 1) // 2, prime_mod) ^ 1 != 0:
            log_parent = int(math.log(prime_mod, maybe_parent))
            while True:
                random_power = random.randint(log_parent // 2, log_parent)
                if math.gcd(random_power, prime_mod - 1) ^ 1 == 0:
                    break
            new_parent = maybe_parent ** random_power
            return new_parent


def prime_num(prime_size):
    while True:
        random_binary_num = [str(round(random.random())) for _ in range(prime_size)]
        random_binary_num[0] = "1"
        random_binary_num[-1] = "1"
        prime_ = int("".join(random_binary_num), 2)
        if sympy.isprime(prime_) is False:
            continue
        else:
            break
    return prime_


def alg_euc(x: int, y: int):
    if x < y:
        mp = x
        x = y
        y = mp
    A = [0, 1]
    B = [1, 0]
    nod, a, b = 0, 0, 0
    while y != 0:
        q = x // y
        r = x - q * y
        a = A[1] - q * A[0]
        b = B[1] - q * B[0]
        x = y
        y = r
        A[1] = A[0]
        A[0] = a
        B[1] = B[0]
        B[0] = b
        nod = x
        a = A[1]
        b = B[1]
    return nod, a, b



