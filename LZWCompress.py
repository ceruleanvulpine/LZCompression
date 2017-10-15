# LZWCompress.py
# Compresses an input file using the LZW algorithm

text = open("input","rb")
dictionary = {}
output = open("output","w")

cur_dictval = 0
cur_string = ""
next_char = ""

# Construct initial dictionary w/all ASCII characters
#for i in range(0,128):
#    dictionary[chr(i)] = cur_dictval
#    cur_dictval = cur_dictval + 1

dictionary = {"a":0, "b":1}
cur_dictval = 2

cur_string = text.read(1)
print(cur_string)
next_char = text.read(1)
print(next_char)
while not next_char ==  "":
    if (cur_string + next_char) in dictionary:
        cur_string = cur_string + next_char
    else:
        output.write(str(dictionary[cur_string]) + "\n")
        dictionary[(cur_string + next_char)] = cur_dictval
        cur_dictval = cur_dictval + 1
        cur_string = next_char
    next_char = text.read(1)
output.write(str(dictionary[cur_string]))
print(dictionary)

text.close()
output.close()
