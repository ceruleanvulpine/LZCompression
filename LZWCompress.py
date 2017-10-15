# LZWCompress.py
# Compresses an input string using the LZW algorithm

text = f.open("input","r")
dictionary = {}
output = f.open("output","w")

cur_dictval = 0
cur_string = ""
cur_stringindex = 0
next_char = ""

# Construct initial dictionary w/all ASCII characters
for i in range(0,128):
    dictionary[chr(i)] = cur_dictval
    cur_dictval = cur_dictval + 1

cur_string = text[0]
cur_stringindex = 1
while cur_stringindex < len(text):
    next_char = text[cur_stringindex]
    cur_stringindex = cur_stringindex + 1
    if (cur_string + next_char) in dictionary:
        cur_string = cur_string + next_char
    else:
        output = output + str(dictionary[cur_string])
        dictionary[(cur_string + next_char)] = cur_dictval
        cur_dictval = cur_dictval + 1
        cur_string = next_char
output = output + str(dictionary[cur_string]) + "\n"
print(output)
print(dictionary)
