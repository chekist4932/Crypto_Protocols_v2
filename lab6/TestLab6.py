
from hmac_sha_gost import hmac_hash
import hashlib
import hmac
from pygost import gost34112012256
from pygost import gost34112012512




msg = "Здорова, мужики. Новеньким буду. Фомой звать.".encode("utf-8")
obj = hmac_hash()

key_byt = obj.generation_key()

print("\nHMAC-SHA-256")
print(hmac.new(key_byt, msg, digestmod=hashlib.sha256).hexdigest())
print(obj.sha_(msg, key_byt, 256).hex())

print("\nHMAC-SHA-512")
print(hmac.new(key_byt, msg, digestmod=hashlib.sha512).hexdigest())
print(obj.sha_(msg, key_byt, 512).hex())

print("\nHMAC-GOST R 34.11-2012 256")
print(hmac.new(key_byt, msg, digestmod=gost34112012256).hexdigest())
print(obj.gost_stribog(msg, key_byt, 256).hex())

print("\nHMAC-GOST R 34.11-2012 512")
print(hmac.new(key_byt, msg, digestmod=gost34112012512).hexdigest())
print(obj.gost_stribog(msg, key_byt, 512).hex())
