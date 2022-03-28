from pygost import gost34112012512
from pygost import gost34112012256


mess = "Привет"
print(gost34112012512.new(mess.encode("utf-8")).hexdigest())
print(gost34112012256.new(mess.encode("utf-8")).hexdigest())


