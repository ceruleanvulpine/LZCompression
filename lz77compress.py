# LZWCompress.py
# Compresses an input file using the LZW algorithm

import heapq as hq
import sys
import huff_functions as huff

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
search = bytes(0)
indices = []

# Fill lookahead buffer with first seven chars
# Note: make this not break for tiny files
lookahead = bytes(7)
for i in range(0, 8):
    lookahead[i] = text.read(1)

while next_char: #have this be while lookahead not empty!!

    # Shift search and lookahead buffers forward one
    if len(search) == 8:
        for i in range(0, 7):
            search[i] = search[i+1]
        search[7] = 
    else:
            
    
    offset = -1;
    for i in range(1, len(search) + 1):
        if search[len(search) - i] == next_char:
            offset = i
            break

    if not offset == -1:
        length = 1
        while next_char == search[len(search) - offset + length]:
            length = length + 1
            next_char = lookahead[next]
        print((offset, length, 0))
    else:
        print((0, 0, next_char))


    next_char = text.read(1)
            
        
        
        
        



output.close()
