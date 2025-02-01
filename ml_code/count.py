with open("data/data.csv", 'r') as f:
    data = [i.strip() for i in f.readlines()]
    


functions = {}
inline = []
no_inline = []

for s in data:
    data_list = s.split("@")
    if data_list[0] not in functions:

        functions[data_list[0]] = ""
        if data_list[-1] == "0":
            no_inline.append(data_list[0])
        if data_list[-1] == "1":
            inline.append(data_list[0])

print(len(functions))  
print(len(inline))          
print(len(no_inline))


