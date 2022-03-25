
from pygost import gost34112012512
print('Привет'.encode("utf-8"))
data_for_signing = 'hello'.encode("utf-8")
dgst = gost34112012512.new(data_for_signing).hexdigest()
print(dgst)


# b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82'
# b'\xd1\x82\xd0\xb5\xd0\xb2\xd0\xb8\xd1\x80\xd0\x9f'
# 82d1b5d0b2d0b8d080d19fd0
# d182d0b5d0b2d0b8d180d09f
