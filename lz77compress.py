# LZWCompress.py
# Compresses an input file using the LZW algorithm

import heapq as hq
import sys
import huff_functions as huff

search_capacity = 8
lookahead_capacity = 7
search_size = 0
lookahead_size = 0

if len(sys.argv) == 3:
    inputname = sys.argv[1]
    outputname = sys.argv[2]
elif len(sys.argv) == 2:
    inputname = sys.argv[1]
    outputname = sys.argv[1] + "_compressed"
else:
    print("Please provide at least one argument")
    sys.exit()

text = open(inputname,"rb")
search = bytearray(search_capacity)
lookahead = bytearray(lookahead_capacity)
indices = []

# Fill lookahead buffer with first [lookahead_capacity] chars
next_char = text.read(1)
while (lookahead_size != lookahead_capacity) and next_char:
    lookahead[lookahead_size] = next_char
    lookahead_size = lookahead_size + 1
    next_char = text.read(1)

# Main compression algorithm loop
while not lookahead_size == 0:

    to_encode = 0

    offset = 0
    for i in range(1, len(search) + 1): # FIX: Be careful, use search_size instead of len_search
        if search[len(search) - i] == lookahead[to_encode]:
            offset = i
            break

    length = 0
    if not offset == 0:
        while (search[len(search) - offset + length] == lookahead[to_encode]) and not to_encode == lookahead_size: # and to_encode doesn't fall out of lookahead buffer
            length = length + 1
            to_encode = to_encode + 1
        print((offset, length, lookahead[to_encode]))
    else:
        print((0, 0, lookahead[to_encode]))

    # Shift lookahead and search buffers by [length] chars
    for i in range(0, len(search) - length):
        search[i] = search[i+length]
    for i in range(0, length):
        search[len(search) - length + i] = lookahead[i]
    for i in range(0, len(lookahead) - length):
        lookahead[i] = lookahead[i + length]
    lookahead_size = lookahead_size - length
    for i in range(0, length) and next_char: # Bad for loop, fix
        lookahead[len(lookahead) - length + i] = next_char
        lookahead_size = lookahead_size + 1
        next_char = text.read(1)
        

output.close()
