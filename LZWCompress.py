# LZWCompress.py
# Compresses an input file using the LZW algorithm

import heapq as hq
import sys
import huff_functions as huff

text = open("banana","rb")
dictionary = {}
indices = []
output = open("output","wb")

cur_dictval = 0
cur_string = ""
next_char = ""

# Construct initial dictionary w/all possible bytes
for i in range(0,256):
    dictionary[i.to_bytes(1,byteorder = "big")] = cur_dictval
    cur_dictval = cur_dictval + 1

# Compress to list of indices with LZW algorithm, building dictionary
# up to 4096 entries
cur_string = text.read(1)
next_char = text.read(1)
while next_char and (cur_dictval < 4096):
    print(next_char)
    if (cur_string + next_char) in dictionary:
        cur_string = cur_string + next_char
    else:
        indices.append(dictionary[cur_string])
        dictionary[(cur_string + next_char)] = cur_dictval
        cur_dictval = cur_dictval + 1
        cur_string = next_char
    next_char = text.read(1)

# If we reach 4096 entries, stop adding more and just use existing dictionary
while next_char:
    print(next_char)
    if (cur_string + next_char) in dictionary:
        cur_string = cur_string + next_char
    else:
        indices.append(dictionary[cur_string])
        cur_string = next_char
    next_char = text.read(1)
    
indices.append(dictionary[cur_string])
print(dictionary)

text.close()

# Build huffman tree of indices for writing to file:
# Count frequencies of each index
freqs = {}
for index in indices:
   if not index in freqs:
       freqs[index] = 1
   else:
       freqs[index] = freqs[index] + 1

# Build forest
forest = huff.build_forest(freqs)
print(forest)

# Build huffman tree from minheap
forest = huff.buildhufftree(forest)
print(forest)

# Build huffman table from huffman tree
huff_table = huff.buildhufftable(forest)
print(huff_table)

# Write number of indices
output.write((cur_dictval).to_bytes(2,byteorder = "big"))

# Write table of frequencies of indices 
for i in range(0, cur_dictval):
    if i in freqs:
        output.write(freqs[i].to_bytes(4, byteorder = "big"))
    else:
        output.write((0).to_bytes(4, byteorder = "big"))

# Write encoded indices
towrite = 0
bits_written = 0
for index in indices:
    code = huff_table[index]
    for char in code:
        if char == "1":
            bit_flicker = 1 << (7-bits_written)
            towrite = towrite | bit_flicker
        bits_written = bits_written + 1

        # when buffer is full, flush and reset
        if bits_written == 8:
            output.write(towrite.to_bytes(1, byteorder = "big"))
            towrite = 0
            bits_written = 0

# Write partially-full buffer
if not bits_written == 0:
    output.write(towrite.to_bytes(1, byteorder = "big"))

output.close()
