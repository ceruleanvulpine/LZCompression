# LZWCompress.py
# Compresses an input file using the LZW algorithm

text = open("dracula","rb")
dictionary = {}
indices = []
output = open("output","w")

cur_dictval = 0
cur_string = ""
next_char = ""

#Construct initial dictionary w/all ASCII characters
for i in range(0,256):
    dictionary[chr(i)] = cur_dictval
    cur_dictval = cur_dictval + 1

cur_string = text.read(1)
next_char = text.read(1)
while not next_char ==  "":
    if (cur_string + next_char) in dictionary:
        cur_string = cur_string + next_char
    else:
        indices.append(dictionary[cur_string])
        dictionary[(cur_string + next_char)] = cur_dictval
        cur_dictval = cur_dictval + 1
        cur_string = next_char
    next_char = text.read(1)
indices.append(dictionary[cur_string])
output.write(indices)

text.close()
output.close()
