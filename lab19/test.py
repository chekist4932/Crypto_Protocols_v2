import pprint

deg_polynomial = 2 * 2
temp = []

for i in range(deg_polynomial):
    line = []
    for j in range(deg_polynomial):
        line.append(f"{i},{j}")
    temp.append(line)

pprint.pprint(temp)
