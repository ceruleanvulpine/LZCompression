# LZWCompress.py
# Compresses an input file using the LZW algorithm

import heapq as hq

text = open("banana","rb")
dictionary = {}
indices = []
output = open("output","w")

cur_dictval = 0
cur_string = ""
next_char = ""

# Construct initial dictionary w/all ASCII characters
for i in range(0,256):
    dictionary[chr(i)] = cur_dictval
    cur_dictval = cur_dictval + 1

# Compress to list of indices with LZW algorithm
cur_string = bytes.decode(text.read(1))
next_char = bytes.decode(text.read(1))
while not next_char ==  "":
    print(next_char)
    if (cur_string + next_char) in dictionary:
        cur_string = cur_string + next_char
    else:
        indices.append(dictionary[cur_string])
        dictionary[(cur_string + next_char)] = cur_dictval
        cur_dictval = cur_dictval + 1
        cur_string = next_char
    next_char = bytes.decode(text.read(1))
indices.append(dictionary[cur_string])

text.close()

# Build huffman tree of indices for writing to file:
# Count frequencies of each index
freqs = {}
for index in indices:
   if not index in freqs:
       freqs[index] = 1
   else:
       freqs[index] = freqs[index] + 1

# Build forest of nodes
forest = []
for node in freqs:
    hq.heappush(forest, ((freqs[node],node)))

print(forest)

# Build huffman tree from minheap
# Encode and write to file

output.close()
