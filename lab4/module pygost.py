from pygost import gost34112012512
from pygost import gost34112012256
import timeit


mess = "ЗДОРОВА ПАПАША"
print(timeit.timeit(lambda : gost34112012512.new(mess.encode("utf-8")).hexdigest(), number=1000))
# print(gost34112012512.new(mess.encode("utf-8")).hexdigest())
# print(gost34112012256.new(mess.encode("utf-8")).hexdigest())




