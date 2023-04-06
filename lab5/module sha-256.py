# import hashlib
#
# #mess = "Когда теряется равновесие твое сознание усталое"
# mess = "Мне бы твои пули переплавить в струны.."
# #mess = "Привет, мама."
# mess = "dgdвпвпркнувм￠"
# h = hashlib.sha256(mess.encode("utf-8"))
# print (h.hexdigest())
#
# "11fb26befaa600a7f852f8e2751cde597b28f8ea119764af2a18e3ed9a8dcc78082e4f3edf6f2b616b01b559fca599f9da208699e33a793a46698b38239c6c53"
#
# "cd3c3ec8bf7356ed115476d7daf8138129cbdd512b0d484aefc396c7fa0cfe3e"
#
# print(type(mess.encode("utf-8")))
# "660b4b4ad485af0ee8c514b7214cc4e68b0df5b2086075a0ccf1508f92cdeb93"
# "660b4b4ad485af0ee8c514b7214cc4e68b0df5b2086075a0ccf1508f92cdeb93"
#
# "54da08d59ea5ccc0636b1558761571980b7694c4cbef61683295b523a981df11"
# "54da08d59ea5ccc0636b1558761571980b7694c4cbef61683295b523a981df11"
#
# "d4d8c51e497988540e71bdc5eb658e0c07efd6544ae0d22f5b1cd8c9034f153c"
# "eb57d3cafdeb444595d48f3f31dffbf686d0f7047588885eaa31d3a107742977"
#
#
# "e15712013486bf392cc829edb67c483e7f8668f03d24ad731817bd6c67b494b9"\
# "dd6a46374785750cb8bd8a39bcbaa6bbfa73e0eb323d1137bc6f3b8a24fdb0d7cf9cceaadfc57a9696449e50316031f68261318a180b05985021d52f179d594e"


# count = 38550
count = 0
res = 1
while True:
    count += 1
    # res = 1
    # for i in range(1, count+):
    #     res *= (1 - (i / pow(2, 30)))
    res *= (1 - (count / pow(2, 30)))
    if res < 0.5:
        print(res)
        print(count)
        break


