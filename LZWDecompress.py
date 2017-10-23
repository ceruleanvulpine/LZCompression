# LZWDecompress.py
# Decompresses an input file using the LZW algorithm

import heapq as hq
import huff_functions as huff
import sys

text = open("output", "rb")
output = open("doutput", "wb")

# Read number of indices
index_count = int.from_bytes(text.read(2), byteorder = "big")

# Read frequencies
freqs = {}
for i in range(0, index_count):
    num = int.from_bytes(text.read(4), byteorder = "big")
    if not num == 0:
        freqs[i] = num
    
print(freqs)

# Build huffman tree from frequencies
forest = huff.build_forest(freqs)
huff_tree = huff.buildhufftree(forest)
print(huff_tree)

# Use huffman tree to decode text to indices
num_codes = huff_tree[0][0]
indices = []
indices_decoded = 0
curr_location = huff_tree[0]
to_read = int.from_bytes(text.read(1), byteorder = "big")
bits_read = 0

while indices_decoded < num_codes:
    if (not curr_location[2]) and (not curr_location[3]):
        indices.append(curr_location[1])
        curr_location = huff_tree[0]
        indices_decoded = indices_decoded + 1

    bit_checker = 1 << (7 - bits_read)
    if not (to_read & bit_checker):
        # Then bit in question is a 0 - go left
        curr_location = curr_location[2]
    else:
        curr_location = curr_location[3]

    bits_read = bits_read + 1
    if bits_read == 8:
        to_read = int.from_bytes(text.read(1), byteorder = "big")
        bits_read = 0

print(indices)

# Now use LZW decompression algorithm to decode list of indices
# First construct initial dictionary w/all possible bytes
dictionary = {}
cur_dictval = 0
for i in range(0,256):
    dictionary[cur_dictval] = i.to_bytes(1,byteorder = "big")
    cur_dictval = cur_dictval + 1

index = indices[0]
previous = dictionary[index]
output.write(previous)

for i in range(1, len(indices)):
    current = indices[i]
    if current in dictionary:
        s = dictionary[current]
    elif current == len(dictionary):
        # s = previous + previous[0]
        new_s = bytearray(len(previous) + 1)
        for j in range(0, len(previous)):
            new_s[j] = previous[j]
        new_s[len(previous)] = previous[0]
        s = bytes(new_s)
    else:
        "There is an error. Cannot proceed."

    output.write(s)

    if cur_dictval < 4096: 
    
        # build "previous + s[0]" to add to dictionary
        entry = bytearray(len(previous) + 1)
        for j in range(0, len(previous)):
            entry[j] = previous[j]
        entry[len(previous)] = s[0]
        entry = bytes(entry)
        print(entry)
        dictionary[cur_dictval] = entry
        cur_dictval = cur_dictval + 1

    previous = s

print(dictionary)
    
text.close()
output.close()
