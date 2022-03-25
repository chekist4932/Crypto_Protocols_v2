import binascii
import time
import datetime
str2 = "dfsdfdfdsfsfsfaa"

print(str2[:1])
#0b0101100
#print(chr("0b1010000"))
t = ord("\n")
print(f"----{chr(t)}-----")
print(chr(int("00101100",2)))

new_m = ""
with open("test.txt",encoding="utf-8") as file:
    mes = file.readlines()
    print(mes)
    print(len("".join(mes)))
for i in mes[0]:
    #print(f"Mark - {ord(i)} - {chr(ord(i))}")
    pass


times = time.ctime(time.time())
time = str(datetime.datetime.now())[:-7]


print(time)
print("-----")
print(bin(ord("o")))
print(bin(ord("о")))
#print(binascii.a2b_uu())

t = ascii("Привет шлюха")
print(t)
"""
with open("work.txt",'w',encoding="utf-8") as title:
    for i in range(256):
        print(f"{i} - {chr(i)}")
        title.write(f"{chr(i)}\n")

print(ord("А"))
print(chr(1040))

def to_bin(num):
    bin = []

    while num != 0:
        num_mp = num
        num = num // 2
        bin.append(str(num_mp % 2))
    bin.reverse()
    return "".join(bin)

for i in range(256):
    bin = to_bin(i)
    if len(bin) < 8:
        while len(bin) != 8:
            bin = "0" + bin
    print(bin)
    
    
ASCII_dict = []
for i in range(128):
    ASCII_dict.append([i, chr(i)])
with open('ASCII_dict.txt', encoding="utf-8") as file_dict:
    for line in file_dict:
        ASCII_dict.append(line.rstrip("\n").rsplit("\t"))

for i in ASCII_dict:
    bin = to_bin(int(i[0]))
    if len(bin) < 8:
        while len(bin) != 8:
            bin = "0" + bin
    i[0] = bin
"""

def ASCII_get():
    def to_bin(num):
        bin = []

        while num != 0:
            num_mp = num
            num = num // 2
            bin.append(str(num_mp % 2))
        bin.reverse()
        return "".join(bin)

    ASCII_dict = []
    for i in range(128):
        ASCII_dict.append([i, chr(i)])
    with open('ASCII_dict.txt', encoding="utf-8") as file_dict:
        for line in file_dict:
            ASCII_dict.append(line.rstrip("\n").rsplit("\t"))

    for i in ASCII_dict:
        bin = to_bin(int(i[0]))
        if len(bin) < 8:
            while len(bin) != 8:
                bin = "0" + bin
        i[0] = bin
    return ASCII_dict


print("-----===+++=====")
t = b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82'
print(t.decode("utf-8"))