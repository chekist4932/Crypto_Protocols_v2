import timeit
import rsa
import struct



(bob_pub, bob_priv) = rsa.newkeys(512)

message = ['abcdertpofgbdnstfgdbb'.encode('utf8'),
           "рруркрувруураврввупкупуавgd".encode("utf-8"),
           "wertyuiopasdfzxcvbnmhвпвлобdвfthапвпа".encode("utf-8")]
for i in message:
    crypto = rsa.encrypt(i, bob_pub)
    message = rsa.decrypt(crypto, bob_priv)
    print("----")
    print(crypto.hex())
    print(message.decode("utf-8"))

t = 10169002682118050088550588215634444304817438402807329084187403534825437483065845831270286109378056874014428022483990036970153135529817162282557792760020673
#print(struct.pack(">Q", t))
byt_len = len( t.to_bytes(t.bit_length()//8, byteorder="big") )

"""

[pow(int.from_bytes(_block, byteorder='big'), pub_key[1], pub_key[0]) for _block in _msg_blocks.copy()]
"""