# LZWCompress.py
# Compresses an input file using the LZW algorithm

import heapq as hq
import sys
import huff_functions as huff

text = open("dracula1","rb")
dictionary = {}
indices = []
output = open("output","wb")

cur_dictval = 0
cur_string = ""
next_char = ""

# Construct initial dictionary w/all possible bytes
for i in range(0,256):
    dictionary[i.to_bytes(1,byteorder = sys.byteorder)] = cur_dictval
    cur_dictval = cur_dictval + 1

# Compress to list of indices with LZW algorithm
cur_string = text.read(1)
next_char = text.read(1)
while next_char:
    print(next_char)
    if (cur_string + next_char) in dictionary:
        cur_string = cur_string + next_char
    else:
        indices.append(dictionary[cur_string])
        dictionary[(cur_string + next_char)] = cur_dictval
        cur_dictval = cur_dictval + 1
        cur_string = next_char
    next_char = text.read(1)
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

# Build forest of nodes of form (frequency, index, left child, right child)
forest = []
for node in freqs:
    hq.heappush(forest, ((freqs[node],node,None,None)))

print(forest)

# Build huffman tree from minheap
placeholder_index = -1
while len(forest) > 1:
    node1 = hq.heappop(forest)
    node2 = hq.heappop(forest)
    hq.heappush(forest, (node1[0] + node2[0], placeholder_index, node1, node2))
    placeholder_index = placeholder_index - 1

print(forest)

# Build huffman table from huffman tree
huff_table = huff.buildhufftable(forest)
print(huff_table)

# Write number of indices
output.write((cur_dictval - 1).to_bytes(4,byteorder = "big"))

# Write table of frequencies of indices 
for i in range(0, cur_dictval):
    if i in freqs:
        output.write(freqs[i].to_bytes(4, byteorder = "big"))
    else:
        output.write((0).to_bytes(4, byteorder = "big"))

# Write encoded indices


output.close()
