# DEFLATE.py
# Compresses files with a DEFLATE-ish algorithm. (Working towards compliance.)

import heapq as hq
import sys
import huff_functions as huff

search_capacity = 32000
search_size = 0

lookahead_capacity = 258
lookahead_size = 0

chars_sent = 0 # Position of next character to send, relative to the start of the file. (Gives a consistent frame of reference for offsets.)

# Read arguments from command line to determine which file to decompress and where to 
if len(sys.argv) == 3:
    inputname = sys.argv[1]
    outputname = sys.argv[2]
elif len(sys.argv) == 2:
    inputname = sys.argv[1]
    outputname = sys.argv[1] + "_deflated"
else:
    print("Please provide at least one argument")
    sys.exit()

# Setup for lookahead and search buffers, and the dictionary "search" (which contains the locations of all the three-length strings encountered)
text = open(inputname, "rb")
search_buffer = bytearray(search_capacity)
lookahead = bytearray(lookahead_capacity)
search = {}

# We use LZ77 algorithm to compute three lists: offsets, lengths and next_chars; will be compressed and sent in triples
offsets = []
lengths = []
next_chars = []

# Fill lookahead buffer with first [lookahead_capacity] chars
next_char = text.read(1)
while (lookahead_size != lookahead_capacity) and next_char:
    lookahead[lookahead_size] = int.from_bytes(next_char, byteorder = "big")
    lookahead_size = lookahead_size + 1
    next_char = text.read(1)

print(lookahead)

# Main LZ77 loop
while not lookahead_size <= 0:

    print("search: " + str(search))
    
    offset = 0
    length = 0
    shift = 0

    # If there are at least three bytes left, search for a match
    if not lookahead_size <= 2:

        # Get first three bytes as string for hashing
        next_three = chr(lookahead[0]) + chr(lookahead[1]) + chr(lookahead[2])

        if not next_three in search:

            print("Sending as literal")
            
            # Send next char as literal
            offsets.append(0)
            lengths.append(0)
            next_chars.append(lookahead[0])
            shift = 1
            
            # String has not been encountered previously, so construct an entry in search with the index of this match
            print("Adding " + next_three + " at index " + str(chars_sent))
            search[next_three] = [chars_sent]

        else:

            print("Attempting to send " + next_three + " as match")
            print(str(search_buffer))
            print(str(lookahead))

            # Look through all matches for the longest recent one
            # NOTE: Take care of case where only matches are >32000 back
            length = 3
            matches = search[next_three]
            offset = chars_sent - matches[0]
            for match in matches:

                print("Examining match at " + str(match))
                
                cur_length = 3
                cur_offset = chars_sent - match

                if not cur_offset >= 32000: 
                
                    # Compare characters [cur_length] into lookahead and [cur_length]
                    # until 1) they don't match 2) we spill out of search buffer
                    # 3) we're matching entire lookahead buffer
                    while cur_offset > cur_length and search_buffer[len(search_buffer) - cur_offset + cur_length] == lookahead[cur_length] and not cur_length == lookahead_size - 1:
                        cur_length = cur_length + 1

                    # Then if 2) happened, compare with beginning of lookahead
                    if cur_offset <= cur_length:

                        print("Spilling over into lookahead buffer...")
                        
                        while lookahead[cur_length - cur_offset] == lookahead[cur_length] and not cur_length == lookahead_size - 1:
                            cur_length = cur_length + 1
                            

                    # If this is new longest match, store it in length/offset
                    if cur_length > length:
                        length = cur_length
                        offset = cur_offset

                print("... which has offset " + str(cur_offset) + " and length " + str(cur_length))
                        
            offsets.append(offset)
            lengths.append(length)
            next_chars.append(lookahead[length])
            shift = length + 1

            # Add this index to the entry for next_string
            # (At the beginning, so search will prioritize more recent matches)
            print("Adding " + next_three + " to search at index " + str(chars_sent))
            search[next_three].insert(0, chars_sent)     

    else:
        # Less than three bytes left, so send as literal
        offsets.append(0)
        lengths.append(0)
        next_chars.append(lookahead[0])
        shift = 1
            
    # Shift lookahead and search buffers, and add three-strings to search as we
    # watch them go by

    # Shift search buffer left by [shift] chars, and fill from lookahead
    for i in range(0, len(search_buffer) - shift):
        search_buffer[i] = search_buffer[i+shift]
    for i in range(0, shift):
        search_buffer[len(search_buffer) - shift + i] = lookahead[i]
    # Increase size of search buffer if not already full
    search_size = search_size + shift
    if search_size >= search_capacity:
        search_size = search_capacity

    # Get and save three-strings up to one that will be examined in next loop
    for i in range(1, shift):
        if i <= lookahead_size - 3:
            next_three = chr(lookahead[i]) + chr(lookahead[i+1]) + chr(lookahead[i+2]);
            print("Examining string " + next_three + " at index " + str(i))

            if next_three in search:
                search[next_three].insert(0, chars_sent + i)
            else:
                search[next_three] = [chars_sent + i]
        else:
            break

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

    chars_sent = chars_sent + shift

# Write an end-of-block character (there will only be one of these right now since it's all in one block)
offsets.append(0)
lengths.append(0)
next_chars.append(256)

print(str(offsets))
print(str(lengths))
print(str(next_chars))
        
# Open output stream; towrite is a one-byte buffer, bits_written keeps track of how much of it is full
output = open(outputname, "wb")
towrite = 0
bits_written = 0

# Currently we are putting all data in one dynamically compressed block
# So write BFINAL = 1 and BTYPE = 10 to the buffer, to signify that it is final and dynamically compressed
bit_flicker = 6 << 5
towrite = towrite | bit_flicker
bits_written = 3

# Constructing huffman tree for lengths and literals
# First count frequencies of codes: 0-255 are literals, 256 is end of block, 257-285 represent lengths (some are ranges of lengths, with extra bits to be placed after symbol)
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
    elif l == 258:
        code = 285

    if code in ll_frequencies:
        ll_frequencies[code] = ll_frequencies[code] + 1
    else:
        ll_frequencies[code] = 1

# Build generic huffman tree from frequencies
ll_forest = huff.build_forest(ll_frequencies)
ll_tree = huff.buildhufftree(ll_forest)

# Get ordered list of code lengths to create canonical huffman code 
ll_codelengths = huff.getcodelengths(ll_tree)
ll_codelengths_list = huff.lengthslist(range(0, 286), ll_codelengths)
print(ll_codelengths_list)
sys.exit()

# Construct list of code length codes for canonical huffman tree for lengths/literals
# See deflate docs for length encoding scheme
prev = -1
repeat_length = 0
codetowrite = 0
codelengthcodes = []
for length in ll_codelengths_list:
    
    # If the code length is a repeat, increase the repeat length
    # If we have reached the limit of repeat size, output code for repeat section
    if prev == length:
        repeat_length = repeat_length + 1
        if 1 <= prev <= 15 and repeat_length == 6:
            # Write repeat code (16) plus code for 6 repeats (3)
            codelengthcodes.append(16)
            codelengthcodes.append(3)
            repeat_length = 0
        elif prev == 0 and repeat_length == 138:
            # Write long zero repeat code (18) plus code for 138 repeats (127)
            codelengthcodes.append(18)
            codelengthcodes.append(127)
            repeat_length = 0

    # If we have changed code lengths, output code for last repeat section if
    # there is one, then output code for new character
    else:
        if repeat_length != 0:
            # NOTE: TO FIX: If repeat length is 1 or 2, just output code more times
            if prev == 0:
                if 3 <= repeat_length <= 10:
                    codelengthcodes.append(17)
                    codelengthcodes.append(repeat_length - 3)
                elif 11 <= repeat_length <= 138:
                    codelengthcodes.append(18)
                    codelengthcodes.append(repeat_length - 11)
            else:
                if 3 <= repeat_length <= 6:
                    codelengthcodes.append(16)
                    codelengthcodes.append(repeat_length - 3)
            repeat_length = 0
        codelengthcodes.append(length)
        prev = length

# Compress THOSE code length codes with ANOTHER canonical huffman code and output

    

# Construct canonical huffman code for length/literal tree

# Repeat this all for distances

# Output compressed data



