import codecs
from struct import unpack
from codecs import getdecoder
from codecs import getencoder
"""
mip
Hello, guys. It's test message for use in your BAD LIFE
hAHahahahahahshahahahahaa
gagagGagGDSgagAGgdgD
My name is FOMA, i'm gay.
"""
"""

def hex_to_bin(stt):
    MMM = ""
    for i in range(0, len(stt), 2):
        char = stt[i:i + 2]
        #print(char)
        bin_char = bin(int(char, 16))[2:]
        while len(bin_char) % 8 != 0:
            bin_char = "0" + bin_char
        MMM += bin_char
    return MMM

mes = "323130393837363534333231303938373635343332313039383736353433323130393837363534333231303938373635343332313039383736353433323130"
#mes = "486f64c1917879417fef082b3381a4e211c324f074654c38823a7b76f830ad00fa1fbae42b1285c0352f227524bc9ab16254288dd6863dccd5b9f54a1ad0541b"
data = "Hello guy"
data = "Привет гайс"
res = ""

# text_to_hex
mp = data.encode("utf-8").hex()
print(mp)



file = open("tex.txt","wb")
file.write(bytes("Привет мама","utf-8"))
file.close()

#print(mp)
#print(mp.encode("hex"))
#print(tt.decode("utf-8"))
print(bytes.fromhex(mes).decode("utf-8"))

for i in data:
    #res += (hex(ord(i.encode("utf-8")))[2:])
    pass
#print(res)


# hex_to_text
MMM = ""
for i in range(0, len(mes), 2):

    char = mes[i:i + 2]
    #print(char)
    MMM += chr(int(char,16))

#print(MMM)




inp = "Hello"
mes = inp[::-1].encode("utf-8").hex()
print("Hello".encode("utf-8").hex())
print(mes)
new = ""
for i in [mes[i:i+2] for i in range(0,len(mes),2)]:
    new += i[::-1]
print(new)
print(new[::-1])
"""
import locale
print(locale.getpreferredencoding())
tex = "н".encode("cp1251")
print(tex)
print(codecs.encode("Привет","utf-8"))
