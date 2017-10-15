# LZWDecompress.py
# Decompresses an input file using the LZW algorithm

indices = open("output", "r")
dictionary = {}
output = open("doutput", "w")

cur_dictval = 0

# Construct initial dictionary w/all ASCII characters
#for i in range(0,128):
#    dictionary[cur_dictval] = chr(i)
#    cur_dictval = cur_dictval + 1

dictionary = {0:"a", 1:"b"}
cur_dictval = 2

result = ""
index = int(indices.readline()[:-1])
previous = dictionary[index]
result = result + previous

current = indices.readline()
while not current == "":
    if len(current) == 2:
        current = current[:-1]
    cur_index = int(current)
    if cur_index in dictionary:
        s = dictionary[cur_index]
    elif cur_index == len(dictionary):
        s = previous + previous[0]
    else:
        "There is an error. Cannot proceed."

    result = result + s
    dictionary[cur_dictval] = previous + s[0]
    cur_dictval = cur_dictval + 1
    previous = s
    current = indices.readline()

print(result)

indices.close()
output.close()
