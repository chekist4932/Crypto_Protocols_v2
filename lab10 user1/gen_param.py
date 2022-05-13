import itertools
import random
import time
import timeit
import math
import sympy


class GenKey:

    def prime_num(self, prime_size):
        while True:
            prime = [str(round(random.random())) for _ in range(prime_size)]
            prime[0] = "1"
            prime[-1] = "1"
            p = int("".join(prime), 2)
            if sympy.isprime(p) is False:
                continue
            else:
                break
        return p

    @staticmethod
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

