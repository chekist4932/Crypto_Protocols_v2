import multiprocessing as mp
import sys
import tqdm
import json
import math


# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
def per(size, num, lit_con, result, que):
    try:
        for k, j in enumerate(range(lit_con[lit_con.index(num) - 1] + 1, num + 1)):
            flag = True
            for i in range(2, int(math.sqrt(size)) + 1):
                if j % i == 0 and j != i:
                    flag = False
            if flag:
                result.append(j)
        que.put("CLOSED!")
        return result
    except KeyboardInterrupt:
        print(f"Презждевременное завершение процесса - {mp.current_process().name}")
        que.put("CLOSED!")
        return result
    except Exception as er:
        print(f"Презждевременное завершение процесса - {mp.current_process().name} | Ошибка завершения - {str(er)} ")
        que.put("CLOSED!")


def call_back(result):

    output = sum(result, [])
    output.sort()
    with open("Primes.json", "w") as file:
        json.dump(output, file, indent=4)


def menu(size, count_proc):
    mp_val = (size // count_proc) + size - ((size // count_proc) * count_proc)
    lit_con = [1]

    for i in range(count_proc):
        lit_con.append(mp_val)
        mp_val += size // count_proc
    result = []
    my_pool = mp.Pool(processes=count_proc)
    mng = mp.Manager()
    que = mng.Queue()
    async_res = my_pool.starmap_async(
        per,
        iterable=[[size, x, lit_con, result, que] for x in lit_con[1:]],
        callback=call_back
    )

    async_res.wait()



if __name__ == "__main__":
    menu(10000, 4)
    with open("Primes.json") as file:
        print(json.load(file))
