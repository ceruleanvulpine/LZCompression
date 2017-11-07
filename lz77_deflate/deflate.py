# DEFLATE.py
# Compresses files with a DEFLATE-ish algorithm. (Working towards compliance.)

import heapq as hq
import sys
import huff_functions as huff

search_capacity = 32000
lookahead_capacity = 258
search_size = 0
lookahead_size = 0

if len(sys.argv) == 3:
    inputname = sys.argv[1]
    outputname = sys.argv[2]
elif len(sys.argv) == 2:
    inputname = sys.argv[1]
    outputname = sys.argv[1] + "_deflated"
else:
    print("Please provide at least one argument")
    sys.exit()

text = open(inputname, "rb")
search = bytearray(search_capacity) # NOTE: This is a dumb inefficient way to do this, replace with hash chained table
lookahead = bytearray(lookahead_capacity)

# Now use LZ77 algorithm to compute lists of output, before compressing
offsets = []
lengths = []
next_chars = []

# Fill lookahead buffer with first [lookahead_capacity] chars
next_char = text.read(1)
while (lookahead_size != lookahead_capacity) and next_char:
    lookahead[lookahead_size] = int.from_bytes(next_char, byteorder = "big")
    lookahead_size = lookahead_size + 1
    next_char = text.read(1)

# Main LZ77 loop
while not lookahead_size <= 0:
    
    to_encode = 0 # TO_ENCODE: first char in lookahead not coded for
    offset = 0
    length = 0
    shift = 0
      
    for i in range(len(search) - search_size, len(search)):
        if search[i] == lookahead[to_encode]:
            offset = len(search) - i
            break

    if not offset == 0:
        length = 1
        to_encode = to_encode + 1
        while offset > length and search[len(search) - offset + length] == lookahead[to_encode] and not to_encode == lookahead_size - 1:
            to_encode = to_encode + 1
            length = length + 1
            # When loop terminates, length = offset or search[len(search) - offset + length] is first char that doesn't match
        if length == offset:
            while lookahead[length - offset] == lookahead[to_encode] and not to_encode == lookahead_size - 1:
                length = length + 1
                to_encode = to_encode + 1
            # When loop terminates, length = to_encode = lookahead_size or lookahead[length - offset] is first char to not match

        # Write offset and length in 1 byte each, and next char in one byte NOTE: change this for possible smaller buffer?
        # NOTE: hacky fix to not use matches of len 1 and 2, fix with hash chaining
        if length == 1 or length == 2:
            offsets.append(0)
            lengths.append(0)
            next_chars.append(lookahead[to_encode - length])
        
        offsets.append(offset)
        lengths.append(length)
        next_chars.append(lookahead[to_encode])

        shift = length + 1
    else:
        offsets.append(0)
        lengths.append(0)
        next_chars.append(lookahead[to_encode])
    
        shift = 1
      
    # Shift lookahead and search buffers

    # Shift search buffer left by [shift] chars, and fill from lookahead
    for i in range(0, len(search) - shift):
        search[i] = search[i+shift]
    for i in range(0, shift):
        search[len(search) - shift + i] = lookahead[i]
    # Increase size of search buffer if not already full
    search_size = search_size + shift
    if search_size >= search_capacity:
        search_size = search_capacity

    # Shift lookahead buffer left by [shift] chars, and fill from text
    for i in range(0, lookahead_size - shift):
        lookahead[i] = lookahead[i + shift]
    lookahead_size = lookahead_size - shift
    for i in range(0, shift):
        if next_char:
            lookahead[len(lookahead) - shift + i] = int.from_bytes(next_char, byteorder = "big")
            lookahead_size = lookahead_size + 1
            next_char = text.read(1)
        else:
            break


output = open(outputname, "wb")
towrite = 0
bits_written = 0

# Currently we are putting all data in one dynamically compressed block
# So write BFINAL = 1 and BTYPE = 10 to the buffer, to signify that it is final and dynamically compressed
bit_flicker = 6 << 5
towrite = towrite | bit_flicker
bits_written = 3

# Now compress the output in offsets, lengths, and next_chars, using huffman coding
# One tree is made for lengths and literals, and another for offsets

# Constructing length and literal tree
# Codes 0-255 are literals; 256 is end of block; 257-285 represent lengths (some represent ranges of lengths, with extra bits after symbol)
# Find frequencies of the things represented by these codes:
ll_frequencies = {}
for nc in next_chars:
    if nc in ll_frequencies:
        ll_frequencies[nc] = ll_frequencies[nc] + 1
    else:
        ll_frequencies[nc] = 1

for l in lengths:
    code = -1
    if l <= 10:
        code = 254 + l
    elif l == 11 or l == 12:
        code = 265
    elif l == 13 or l == 14:
        code = 266
    elif l == 15 or l == 16:
        code = 267
    elif l == 17 or l == 18:
        code = 268
    elif l >= 19 and l <= 22:
        code = 269
    elif l >= 23 and l <= 26:
        code = 270
    elif l >= 27 and l <= 30:
        code = 271
    elif l >= 31 and l <= 34:
        code = 272
    elif l >= 35 and l <= 42:
        code = 273
    elif l >= 43 and l <= 50:
        code = 274
    elif l >= 51 and l <= 58:
        code = 275
    elif l >= 59 and l <= 66:
        code = 276
    elif l >= 67 and l <= 82:
        code = 277
    elif l >= 83 and l <= 98:
        code = 278
    elif l >= 99 and l <= 114:
        code = 279
    elif l >= 115 and l <= 130:
        code = 280
    elif l >= 131 and l <= 162:
        code = 281
    elif l >= 163 and l <= 194:
        code = 282
    elif l >= 195 and l <= 226:
        code = 283
    elif l >= 227 and l <= 257:
        code = 284
    elif l == 285:
        code = 285

    if code in ll_frequencies:
        ll_frequencies[code] = ll_frequencies[code] + 1
    else:
        ll_frequencies[code] = 1

print(ll_frequencies)

ll_forest = huff.build_forest(ll_frequencies)
print(ll_forest)
ll_tree = huff.buildhufftree(ll_forest)
print(ll_tree)
ll_codelengths = huff.getcodelengths(ll_tree)
print(ll_codelengths)
