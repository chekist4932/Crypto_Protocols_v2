s = [252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77, 233,
     119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193, 249, 24,
     101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79, 5, 132, 2, 174, 227,
     106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31, 235, 52, 44, 81, 234, 200, 72,
     171, 242, 42, 104, 162, 253, 58, 206, 204, 181, 112, 14, 86, 8, 12, 118, 18, 191,
     114, 19, 71, 156, 183, 93, 135, 21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120,
     111, 157, 158, 178, 177, 50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195,
     189, 13, 87, 223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185,
     3, 224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74, 167, 151,
     96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65, 173, 69, 70, 146, 39, 94,
     85, 47, 140, 163, 165, 125, 105, 213, 149, 59, 7, 88, 179, 64, 134, 172, 29, 247, 48,
     55, 107, 228, 136, 217, 231, 137, 225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170,
     144, 202, 216, 133, 97, 32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229,
     108, 82, 89, 166, 116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182]

p = [0, 8, 16, 24, 32, 40, 48, 56, 1, 9, 17, 25, 33, 41, 49, 57, 2, 10, 18, 26, 34, 42, 50, 58,
     3, 11, 19, 27, 35, 43, 51, 59, 4, 12, 20, 28, 36, 44, 52, 60, 5, 13, 21, 29, 37, 45, 53,
     61, 6, 14, 22, 30, 38, 46, 54, 62, 7, 15, 23, 31, 39, 47, 55, 63]

l = ['8e20faa72ba0b470', '47107ddd9b505a38', 'ad08b0e0c3282d1c', 'd8045870ef14980e', '6c022c38f90a4c07',
     '3601161cf205268d', '1b8e0b0e798c13c8', '83478b07b2468764', 'a011d380818e8f40', '5086e740ce47c920',
     '2843fd2067adea10', '14aff010bdd87508', '0ad97808d06cb404', '05e23c0468365a02', '8c711e02341b2d01',
     '46b60f011a83988e', '90dab52a387ae76f', '486dd4151c3dfdb9', '24b86a840e90f0d2', '125c354207487869',
     '092e94218d243cba', '8a174a9ec8121e5d', '4585254f64090fa0', 'accc9ca9328a8950', '9d4df05d5f661451',
     'c0a878a0a1330aa6', '60543c50de970553', '302a1e286fc58ca7', '18150f14b9ec46dd', '0c84890ad27623e0',
     '0642ca05693b9f70', '0321658cba93c138', '86275df09ce8aaa8', '439da0784e745554', 'afc0503c273aa42a',
     'd960281e9d1d5215', 'e230140fc0802984', '71180a8960409a42', 'b60c05ca30204d21', '5b068c651810a89e',
     '456c34887a3805b9', 'ac361a443d1c8cd2', '561b0d22900e4669', '2b838811480723ba', '9bcf4486248d9f5d',
     'c3e9224312c8c1a0', 'effa11af0964ee50', 'f97d86d98a327728', 'e4fa2054a80b329c', '727d102a548b194e',
     '39b008152acb8227', '9258048415eb419d', '492c024284fbaec0', 'aa16012142f35760', '550b8e9e21f7a530',
     'a48b474f9ef5dc18', '70a6a56e2440598e', '3853dc371220a247', '1ca76e95091051ad', '0edd37c48a08a6d8',
     '07e095624504536c', '8d70c431ac02a736', 'c83862965601dd1b', '641c314b2b8ee083']

C = ['b1085bda1ecadae9ebcb2f81c0657c1f2f6a76432e45d016714eb88d7585c4fc4b7ce09192676901a2422a08a460d31505767436cc744d23dd806559f2a64507',
     '6fa3b58aa99d2f1a4fe39d460f70b5d7f3feea720a232b9861d55e0f16b501319ab5176b12d699585cb561c2db0aa7ca55dda21bd7cbcd56e679047021b19bb7',
     'f574dcac2bce2fc70a39fc286a3d843506f15e5f529c1f8bf2ea7514b1297b7bd3e20fe490359eb1c1c93a376062db09c2b6f443867adb31991e96f50aba0ab2',
     'ef1fdfb3e81566d2f948e1a05d71e4dd488e857e335c3c7d9d721cad685e353fa9d72c82ed03d675d8b71333935203be3453eaa193e837f1220cbebc84e3d12e',
     '4bea6bacad4747999a3f410c6ca923637f151c1f1686104a359e35d7800fffbdbfcd1747253af5a3dfff00b723271a167a56a27ea9ea63f5601758fd7c6cfe57',
     'ae4faeae1d3ad3d96fa4c33b7a3039c02d66c4f95142a46c187f9ab49af08ec6cffaa6b71c9ab7b40af21f66c2bec6b6bf71c57236904f35fa68407a46647d6e',
     'f4c70e16eeaac5ec51ac86febf240954399ec6c7e6bf87c9d3473e33197a93c90992abc52d822c3706476983284a05043517454ca23c4af38886564d3a14d493',
     '9b1f5b424d93c9a703e7aa020c6e41414eb7f8719c36de1e89b4443b4ddbc49af4892bcb929b069069d18d2bd1a5c42f36acc2355951a8d9a47f0dd4bf02e71e',
     '378f5a541631229b944c9ad8ec165fde3a7d3a1b258942243cd955b7e00d0984800a440bdbb2ceb17b2b8a9aa6079c540e38dc92cb1f2a607261445183235adb',
     'abbedea680056f52382ae548b2e4f3f38941e71cff8a78db1fffe18a1b3361039fe76702af69334b7a1e6c303b7652f43698fad1153bb6c374b4c7fb98459ced',
     '7bcd9ed0efc889fb3002c6cd635afe94d8fa6bbbebab076120018021148466798a1d71efea48b9caefbacd1d7d476e98dea2594ac06fd85d6bcaa4cd81f32d1b',
     '378ee767f11631bad21380b00449b17acda43c32bcdf1d77f82012d430219f9b5d80ef9d1891cc86e71da4aa88e12852faf417d5d9b21b9948bc924af11bd720']



def to_8_bit(elem):
    while len(elem) % 8 != 0:
        elem = "0" + elem
    return elem

def hex_to_bin(stt):
    MMM = ""
    for i in range(0, len(stt), 2):
        char = stt[i:i + 2]
        bin_char = bin(int(char, 16))[2:]

        bin_char = to_8_bit(bin_char)

        MMM += bin_char
    return MMM

def bin_to_hex(res):
    he = ""
    for i in [res[x:x + 8] for x in range(0, len(res), 8)]:
        he += hex(int(i, 2))[2:].zfill(2)
    return he

def sum(vec_1:str,vec_2:str, dimension):
    res = ''
    for i in range(dimension):
        res += str( ( int(vec_1[i]) + int(vec_2[i]) ) % 2 )

    #print(f"\niter - {iter}\nvec1 - {vec_1} |\nvec2 - {vec_2} |\nsum1 - {res}")
    return res


def s_trans(bin_mes, s):
    s_res = []
    for i in [bin_mes[i:i + 8] for i in range(0, len(bin_mes), 8)]:
        s_res.append(hex(s[int(i, 2)]))
    return s_res

def p_trans(s_res, p):
    #p_res = [0 for x in range(64)]
    p_res = [0]*64
    for k, i in enumerate(s_res):
        # place = p[k]
        p_res[k] = s_res[p[k]]
    return p_res


def l_trans(p_res,l):
    #mp = ""
    mp_vec = []
    for i in p_res:
        elem = bin(int(i, 16))[2:]
        elem = to_8_bit(elem)
        mp_vec.append(elem)
    c_vec = ["".join(mp_vec[i:i + 8]) for i in range(0, len(mp_vec), 8)]

    del mp_vec

    res_list = []

    for i in range(8):
        mp_list = []
        for k, j in enumerate(c_vec[i]):
            if j == "1":
                mp_list.append(hex_to_bin(l[k]))
                # print(f"c_vec_ind - {k} | bit - {j} | {l[k]}")
            elif j == "0":
                mp_list.append("0" * 64)

        res_list.append(mp_list)

    del mp_list

    l_res = []
    for k in res_list:
        res = ''
        #he = ""
        mp = k[0]
        for i in range(1, 64):
            res = sum(mp, k[i], 64)
            mp = res
        """
        for i in [res[x:x + 8] for x in range(0, len(res), 8)]:
            he += hex(int(i, 2))[2:].zfill(2)
            # print(f"num - {int(i, 2)} | hex - {hex(int(i, 2))[2:].zfill(2)}")
        """
        he = bin_to_hex(res)
        l_res.append(he)

    del res_list
    return l_res


def LPS(bin_mes,s,p,l):
    return "".join(l_trans(p_trans(s_trans(bin_mes,s),p),l))


def X_trans(k,m): # bin,bin
    sum_ = sum(k,m,512)
    return bin_to_hex(sum_)


def E_trans(k1,m): # hex, bin
    k = [0] * 13
    k[0] = k1
    for i in range(1, 13):
        k[i] = LPS(hex_to_bin(X_trans(hex_to_bin(k[i - 1]), hex_to_bin(C[i - 1]))), s, p, l)

    for j in range(13):
        if j == 12:
            m = hex_to_bin(X_trans(hex_to_bin(k[j]), m))
            break
        m = hex_to_bin(X_trans(hex_to_bin(k[j]), m))
        m = hex_to_bin(LPS(m, s, p, l))

    return bin_to_hex(m)

def g_N(h,m,N): # bin,bin,bin
    k1 = LPS(sum(h, N, 512), s, p, l)
    e_res = E_trans(k1, m)
    h = sum(  sum(hex_to_bin(e_res),h,512)   ,m ,512)

    return h  # bin




#   k1 = LPS(h+N)
#   k1 + m
#   LPS(k1+m)
#
#



'''




m = "00000001001100100011000100110000001110010011100000110111001101100011010100110100001" \
    "10011001100100011000100110000001110010011100000110111001101100011010100110100001100" \
    "110011001000110001001100000011100100111000001101110011011000110101001101000011001100" \
    "1100100011000100110000001110010011100000110111001101100011010100110100001100110011001" \
    "000110001001100000011100100111000001101110011011000110101001101000011001100110010001" \
    "100010011000000111001001110000011011100110110001101010011010000110011001100100011000100110000"
h = "0" * 512
N = "0" * 512
E = "0" * 512
print(  bin_to_hex(g_N(h,m,N))    )
N  = bin((int(N,2) + 512 ) % 2**512)[2:]
while len(N) % 512 !=0:
    N = "0" + N
#print(f"{N}\n{len(N)}")


E  = bin((int(E,2) + int(m,2) ) % 2**512)[2:]

while len(E) % 512 !=0:
    E = "0" + E
print(f"{E}\n{len(E)}")
#print(bin_to_hex(m))
#k1 = LPS(sum(h,N,512), s, p, l)
#E_trans(k1,m)

'''

#print(LPS(x,s,p,l))
#print ( X_trans (hex_to_bin(k1) , hex_to_bin(C[0])   ) )
# 128 bytes
# 512 bits
#print("".join([x[2:] for x in s_res]))
#print("".join([x[2:] for x in p_res]))

#print("".join(l_res))

"b383fc2eced4a574b383fc2eced4a574b383fc2eced4a574b383fc2eced4a574b383fc2eced4a574b383fc2eced4a574b383fc2eced4a574b383fc2eced4a574"
"b383fc2eced4a574b383fc2eced4a574b383fc2eced4a574b383fc2eced4a574b383fc2eced4a574b383fc2eced4a574b383fc2eced4a574b383fc2eced4a574"

"""
b2 = 10110010
bi = 01000001
b3 = 10110011
f35b0d889eadfcff73b6b17f33413a97417d96f0c4cc9d30cda8ebb7dcd5d1b061e620bac75b367370605f474ddc006003bec4c4d7ce59a73fbe6766934c55a2
f35b0d889eadfcff73b6b17f33413a97417d96f0c4cc9d30cda8ebb7dcd5d1b061e620bac75b367370605f474ddc006003bec4c4d7ce59a73fbe6766934c55a2
c1 = "b1085bda1ecadae9ebcb2f81c0657c1f2f6a76432e45d016714eb88d7585c4fc" \
     "4b7ce09192676901a2422a08a460d31505767436cc744d23dd806559f2a64507"
c2 = "6fa3b58aa99d2f1a4fe39d460f70b5d7f3feea720a232b9861d55e0f16b50131" \
     "9ab5176b12d699585cb561c2db0aa7ca55dda21bd7cbcd56e679047021b19bb7"
c3 = "f574dcac2bce2fc70a39fc286a3d843506f15e5f529c1f8bf2ea7514b1297b7b" \
     "d3e20fe490359eb1c1c93a376062db09c2b6f443867adb31991e96f50aba0ab2"
c4 = "ef1fdfb3e81566d2f948e1a05d71e4dd488e857e335c3c7d9d721cad685e353f" \
     "a9d72c82ed03d675d8b71333935203be3453eaa193e837f1220cbebc84e3d12e"
c5 = "4bea6bacad4747999a3f410c6ca923637f151c1f1686104a359e35d7800fffbd" \
     "bfcd1747253af5a3dfff00b723271a167a56a27ea9ea63f5601758fd7c6cfe57"
c6 = "ae4faeae1d3ad3d96fa4c33b7a3039c02d66c4f95142a46c187f9ab49af08ec6" \
     "cffaa6b71c9ab7b40af21f66c2bec6b6bf71c57236904f35fa68407a46647d6e"
c7 = "f4c70e16eeaac5ec51ac86febf240954399ec6c7e6bf87c9d3473e33197a93c9" \
     "0992abc52d822c3706476983284a05043517454ca23c4af38886564d3a14d493"
c8 = "9b1f5b424d93c9a703e7aa020c6e41414eb7f8719c36de1e89b4443b4ddbc49a" \
     "f4892bcb929b069069d18d2bd1a5c42f36acc2355951a8d9a47f0dd4bf02e71e"
c9 = "378f5a541631229b944c9ad8ec165fde3a7d3a1b258942243cd955b7e00d0984" \
      "800a440bdbb2ceb17b2b8a9aa6079c540e38dc92cb1f2a607261445183235adb"
c10 = "abbedea680056f52382ae548b2e4f3f38941e71cff8a78db1fffe18a1b336103" \
      "9fe76702af69334b7a1e6c303b7652f43698fad1153bb6c374b4c7fb98459ced"
c11 = "7bcd9ed0efc889fb3002c6cd635afe94d8fa6bbbebab07612001802114846679" \
      "8a1d71efea48b9caefbacd1d7d476e98dea2594ac06fd85d6bcaa4cd81f32d1b"
c12 = "378ee767f11631bad21380b00449b17acda43c32bcdf1d77f82012d430219f9b" \
      "5d80ef9d1891cc86e71da4aa88e12852faf417d5d9b21b9948bc924af11bd720"

C = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12]




bin_mes = "0" * 512

s_res = []
p_res = [0 for x in range(64)]
for i in [bin_mes[i:i + 8] for i in range(0, len(bin_mes), 8)]:
    #print(hex(s[int(i,2)]))
    s_res.append(hex(s[int(i,2)]))


for k,i in enumerate(s_res):
    #place = p[k]
    p_res[k] = s_res[p[k]]



mp = ""
mp_vec = []
for i in p_res:
    elem = bin(int(i,16))[2:]
    elem = to_8_bit(elem)
    mp_vec.append(elem)
c_vec = ["".join(mp_vec[i:i + 8]) for i in range(0, len(mp_vec), 8)]




#l = [[142, 32, 250, 167, 43, 160, 180, 112], [71, 16, 125, 221, 155, 80, 90, 56], [173, 8, 176, 224, 195, 40, 45, 28], [216, 4, 88, 112, 239, 20, 152, 14], [108, 2, 44, 56, 249, 10, 76, 7], [54, 1, 22, 28, 242, 5, 38, 141], [27, 142, 11, 14, 121, 140, 19, 200], [131, 71, 139, 7, 178, 70, 135, 100], [160, 17, 211, 128, 129, 142, 143, 64], [80, 134, 231, 64, 206, 71, 201, 32], [40, 67, 253, 32, 103, 173, 234, 16], [20, 175, 240, 16, 189, 216, 117, 8], [10, 217, 120, 8, 208, 108, 180, 4], [5, 226, 60, 4, 104, 54, 90, 2], [140, 113, 30, 2, 52, 27, 45, 1], [70, 182, 15, 1, 26, 131, 152, 142], [144, 218, 181, 42, 56, 122, 231, 111], [72, 109, 212, 21, 28, 61, 253, 185], [36, 184, 106, 132, 14, 144, 240, 210], [18, 92, 53, 66, 7, 72, 120, 105], [9, 46, 148, 33, 141, 36, 60, 186], [138, 23, 74, 158, 200, 18, 30, 93], [69, 133, 37, 79, 100, 9, 15, 160], [172, 204, 156, 169, 50, 138, 137, 80], [157, 77, 240, 93, 95, 102, 20, 81], [192, 168, 120, 160, 161, 51, 10, 166], [96, 84, 60, 80, 222, 151, 5, 83], [48, 42, 30, 40, 111, 197, 140, 167], [24, 21, 15, 20, 185, 236, 70, 221], [12, 132, 137, 10, 210, 118, 35, 224], [6, 66, 202, 5, 105, 59, 159, 112], [3, 33, 101, 140, 186, 147, 193, 56], [134, 39, 93, 240, 156, 232, 170, 168], [67, 157, 160, 120, 78, 116, 85, 84], [175, 192, 80, 60, 39, 58, 164, 42], [217, 96, 40, 30, 157, 29, 82, 21], [226, 48, 20, 15, 192, 128, 41, 132], [113, 24, 10, 137, 96, 64, 154, 66], [182, 12, 5, 202, 48, 32, 77, 33], [91, 6, 140, 101, 24, 16, 168, 158], [69, 108, 52, 136, 122, 56, 5, 185], [172, 54, 26, 68, 61, 28, 140, 210], [86, 27, 13, 34, 144, 14, 70, 105], [43, 131, 136, 17, 72, 7, 35, 186], [155, 207, 68, 134, 36, 141, 159, 93], [195, 233, 34, 67, 18, 200, 193, 160], [239, 250, 17, 175, 9, 100, 238, 80], [249, 125, 134, 217, 138, 50, 119, 40], [228, 250, 32, 84, 168, 11, 50, 156], [114, 125, 16, 42, 84, 139, 25, 78], [57, 176, 8, 21, 42, 203, 130, 39], [146, 88, 4, 132, 21, 235, 65, 157], [73, 44, 2, 66, 132, 251, 174, 192], [170, 22, 1, 33, 66, 243, 87, 96], [85, 11, 142, 158, 33, 247, 165, 48], [164, 139, 71, 79, 158, 245, 220, 24], [112, 166, 165, 110, 36, 64, 89, 142], [56, 83, 220, 55, 18, 32, 162, 71], [28, 167, 110, 149, 9, 16, 81, 173], [14, 221, 55, 196, 138, 8, 166, 216], [7, 224, 149, 98, 69, 4, 83, 108], [141, 112, 196, 49, 172, 2, 167, 54], [200, 56, 98, 150, 86, 1, 221, 27], [100, 28, 49, 75, 43, 142, 224, 131]]




res_list = []

for i in range(8):
    mp_list = []
    for k,j in enumerate(c_vec[i]):
        if j == "1":
            mp_list.append(hex_to_bin(l[k]))
            #print(f"c_vec_ind - {k} | bit - {j} | {l[k]}")
        elif j == "0":
            mp_list.append( "0" * 64 )

    res_list.append(mp_list)






#print(res_list,'\n', len(res_list), '\t', len(res_list[0]))


l_res = []
for k in res_list:
    res = ''
    he = ""
    mp = k[0]
    for i in range(1, 64):
        res = sum(mp, k[i], i)
        mp = res

    for i in [res[x:x + 8] for x in range(0, len(res), 8)]:
        he += hex(int(i, 2))[2:].zfill(2)
        #print(f"num - {int(i, 2)} | hex - {hex(int(i, 2))[2:].zfill(2)}")

    l_res.append(he)



"""



