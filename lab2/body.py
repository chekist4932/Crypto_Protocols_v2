import datetime


def hex_to_bin(stt):
    MMM = ""
    for i in range(0, len(stt), 2):
        char = stt[i:i + 2]
        bin_char = bin(int(char, 16))[2:].zfill(8)
        MMM += bin_char
    return MMM

def bin_to_hex(res):
    he = ""
    for i in [res[x:x + 8] for x in range(0, len(res), 8)]:
        he += hex(int(i, 2))[2:].zfill(2)
    return he


#BASE64
def encode_BASE64(mess):

    BASE64_dict = []
    mess = mess.encode("utf-8")
    mess = mess.hex()
    bin_mes = hex_to_bin(mess)

    count = 0


    if len((bin_mes)) % 24 == 0:
        pass
    else:
        while len((bin_mes)) % 24 != 0:
            bin_mes += '0'
            count += 1

    MES_array = [bin_mes[i:i+6] for i in range(0,len(bin_mes),6)]

    new_mes = ""
    file_dict = open("BASE64_dict.txt","r")
    for line in file_dict:
        r = line.strip().rsplit("\t")
        BASE64_dict.append(r)
    file_dict.close()

    for num,char in enumerate(MES_array):
        for const in BASE64_dict:
            if char == const[0]:
                new_mes+=const[1]

    if count == 8:
        output = new_mes[:-1] + "="
    elif count == 16:
        output = new_mes[:-2] + "=="
    else:
        output = new_mes

    Save_res(output,"Encode on BASE64","enc64")
    print(output)
    return output

def decode_BASE64(cod_mes):

    BASE64_dict = []
    file_dict = open("BASE64_dict.txt", "r")
    for line in file_dict:
        r = line.strip().rsplit("\t")
        BASE64_dict.append(r)
    file_dict.close()
    bin_mes = ""
    for char in cod_mes:
        for i in BASE64_dict:
            if char == i[1]:
                bin_mes += i[0]
                break
    if cod_mes.count("=") == 1:
        bin_mes = bin_mes[:-2]
    elif cod_mes.count("=") == 2:
        bin_mes = bin_mes[:-4]
    MES_array = [bin_mes[i:i + 8] for i in range(0, len(bin_mes), 8)]

    mes = bin_to_hex("".join(MES_array))
    mes = bytes.fromhex(mes).decode("utf-8")

    Save_res(mes, "Decode on BASE64","dec64")
    print(mes)

    return mes

#BASE32
def encode_BASE32(mess):
    BASE32_dict = []
    mess = mess.encode("utf-8").hex()
    bin_mes = hex_to_bin(mess)

    count = 0
    if len((bin_mes)) % 40 == 0:
        pass
    else:
        while len((bin_mes)) % 5 != 0:
            bin_mes += '0'
            count += 1

    MES_array = [bin_mes[i:i+5] for i in range(0,len(bin_mes),5)]

    new_mes = ""
    file_dict = open("BASE32_dict.txt","r")
    for line in file_dict:
        r = line.strip().rsplit("\t")
        BASE32_dict.append(r)
    file_dict.close()

    for num,char in enumerate(MES_array):
        for const in BASE32_dict:
            if char == const[0]:
                new_mes+=const[1]

    if (len(bin_mes) - count) % 5 == 3:
        new_mes += "======"
    elif (len(bin_mes) - count) % 5 == 1:
        new_mes +=  "===="
    elif (len(bin_mes) - count) % 5 == 4:
        new_mes += "==="
    elif (len(bin_mes) - count) % 5 == 2:
        new_mes += "="


    Save_res(new_mes, "Encode on BASE32","enc32")
    print(new_mes)
    return new_mes

def decode_BASE32(cod_mes):
    BASE32_dict = []
    file_dict = open("BASE32_dict.txt", "r")
    for line in file_dict:
        r = line.strip().rsplit("\t")
        BASE32_dict.append(r)
    file_dict.close()

    bin_mes = ""

    for char in cod_mes:
        for i in BASE32_dict:
            if char == i[1]:
                bin_mes += i[0]
    if cod_mes.count("=") == 6:
        bin_mes = bin_mes[:-2]
    elif cod_mes.count("=") == 4:
        bin_mes = bin_mes[:-4]
    elif cod_mes.count("=") == 3:
        bin_mes = bin_mes[:-1]
    elif cod_mes.count("=") == 1:
        bin_mes = bin_mes[:-3]
    MES_array = [bin_mes[i:i + 8] for i in range(0, len(bin_mes), 8)]

    mes = bin_to_hex("".join(MES_array))
    mes = bytes.fromhex(mes).decode("utf-8")

    Save_res(mes, "Decode on BASE32","dec32")
    print(mes)
    return mes


def Save_res(text:str,title:str,mode:str):
    date = str(datetime.datetime.now())[:-7].replace(":","-")
    with open(f"{mode}-ses {date}.txt", "w", encoding="utf-8") as file:
        x = "=" * 20
        file.write(f"{x}{title}{x}\n{text}")
    print("File created.\n")



