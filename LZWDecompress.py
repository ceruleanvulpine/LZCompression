# LZWDecompress.py
# Decompresses an input file using the LZW algorithm

import heapq as hq
import huff_functions as huff

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

# Use huffman tree to decode text to indices
num_codes = huff_tree[0][0]
indices = []
indices_decoded = 0
curr_location = huff_tree[0]
to_read = int.from_bytes(text.read(1), byteorder = "big")
bits_read = 0

while indices_decoded < num_codes:
    if (not curr_location[2]) and (not curr_location[3]):
        indices.append(curr_location[0])
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
        print(p)
        to_read = int.from_bytes(p, byteorder = "big")
        bits_read = 0

print(indices)

