# DEFLATE_FNS.py
# Handy helper functions for DEFLATE.

# Given an integer length between 3 and 258, returns a tuple (code, extra bits)
# according to the scheme outlined in DEFLATE docs
def length_code(l):  
    code = -1
    extrabits = -1
    if l <= 10:
        code = 254 + l
    elif l == 11 or l == 12:
        code = 265
        extrabits = l - 11
    elif l == 13 or l == 14:
        code = 266
        extrabits = l - 13
    elif l == 15 or l == 16:
        code = 267
        extrabits = l - 15
    elif l == 17 or l == 18:
        code = 268
        extrabits = l - 17
    elif l >= 19 and l <= 22:
        code = 269
        extrabits = l - 19
    elif l >= 23 and l <= 26:
        code = 270
        extrabits = l - 23
    elif l >= 27 and l <= 30:
        code = 271
        extrabits = l - 27
    elif l >= 31 and l <= 34:
        code = 272
        extrabits = l - 31
    elif l >= 35 and l <= 42:
        code = 273
        extrabits = l - 35
    elif l >= 43 and l <= 50:
        code = 274
        extrabits = l - 43
    elif l >= 51 and l <= 58:
        code = 275
        extrabits = l - 51
    elif l >= 59 and l <= 66:
        code = 276
        extrabits = l - 59
    elif l >= 67 and l <= 82:
        code = 277
        extrabits = l - 67
    elif l >= 83 and l <= 98:
        code = 278
        extrabits = l - 83
    elif l >= 99 and l <= 114:
        code = 279
        extrabits = l - 99
    elif l >= 115 and l <= 130:
        code = 280
        extrabits = l - 115
    elif l >= 131 and l <= 162:
        code = 281
        extrabits = l - 131
    elif l >= 163 and l <= 194:
        code = 282
        extrabits = l - 163
    elif l >= 195 and l <= 226:
        code = 283
        extrabits = l - 195
    elif l >= 227 and l <= 257:
        code = 284
        extrabits = l - 227
    elif l == 258:
        code = 285

    return (code, extrabits)


# Given an integer length between 3 and 258, returns the number of extra bits that follow the code for that length
def length_code_num_extrabits(l)
    if l <= 10:
        return 0
    elif l >= 11 and l <= 18:
        return 1
    elif l >= 19 and l <= 34:
        return 2
    elif l >= 35 and l <= 66:
        return 3
    elif l >= 67 and l <= 130:
        return 4
    elif l >= 131 and l <= 257:
        return 5
    elif l == 258:
        return 0

# Given an integer distance between 1 and 32768, returns a tuple (code, extra bits)
# according to the scheme outlined in DEFLATE docs
def dist_code(dist):
    code = -1
    extrabits = -1

    if dist == 1:
        code = 0
    elif dist == 2:
        code = 1
    elif dist == 3:
        code = 2
    elif dist == 4:
        code = 3
    elif dist == 5 or dist == 6:
        code = 4
        extrabits = dist - 5
    elif dist == 7 or dist == 8:
        code = 5
        extrabits = dist - 7
    elif dist >= 9 and dist <= 12:
        code = 6
        extrabits = dist - 9
    elif dist >= 13 and dist <= 16:
        code = 7
        extrabits = dist - 13
    elif dist >= 17 and dist <= 24:
        code = 8
        extrabits = dist - 17
    elif dist >= 25 and dist <= 32:
        code = 9
        extrabits = dist - 25
    elif dist >= 33 and dist <= 48:
        code = 10
        extrabits = dist - 33
    elif dist >= 49 and dist <= 64:
        code = 11
        extrabits = dist - 49
    elif dist >= 65 and dist <= 96:
        code = 12
        extrabits = dist - 65
    elif dist >= 97 and dist <= 128:
        code = 13
        extrabits = dist - 97
    elif dist >= 129 and dist <= 192:
        code = 14
        extrabits = dist - 129
    elif dist >= 193 and dist <= 256:
        code = 15
        extrabits = dist - 193
    elif dist >= 257 and dist <= 384:
        code = 16
        extrabits = dist - 257
    elif dist >= 385 and dist <= 512:
        code = 17
        extrabits = dist - 385
    elif dist >= 513 and dist <= 768:
        code = 18
        extrabits = dist - 513
    elif dist >= 769 and dist <= 1024:
        code = 19
        extrabits = dist - 769
    elif dist >= 1025 and dist <= 1536:
        code = 20
        extrabits = dist - 1025
    elif dist >= 1537 and dist <= 2048:
        code = 21
        extrabits = dist - 1537
    elif dist >= 2049 and dist <= 3072:
        code = 22
        extrabits = dist - 2049
    elif dist >= 3073 and dist <= 4096:
        code = 23
        extrabits = dist - 3073
    elif dist >= 4097 and dist <= 6144:
        code = 24
        extrabits = dist - 4097
    elif dist >= 6145 and dist <= 8192:
        code = 25
        extrabits = dist - 6145
    elif dist >= 8193 and dist <= 12288:
        code = 26
        extrabits = dist - 8193
    elif dist >= 12289 and dist <= 16384:
        code = 27
        extrabits = dist - 12289
    elif dist >= 16385 and dist <= 24576:
        code = 28
        extrabits = dist - 16385
    elif dist >= 24577 and dist <= 32768:
        code = 29
        extrabits = dist - 24577

    return (code, extrabits)

# Given a distance between 1 and 32768, returns the number of extra bits that follow the code for that distance
def dist_code_num_extrabits(dist):
    if dist >= 1 and dist <= 4:
        return 0
    elif dist >= 5 and dist <= 8:
        return 1
    elif dist >= 9 and dist <= 16:
        return 2
    elif dist >= 17 and dist <= 32:
        return 3
    elif dist >= 33 and dist <= 64:
        return 4
    elif dist >= 65 and dist <= 128:
        return 5
    elif dist >= 129 and dist <= 256:
        return 6
    elif dist >= 257 and dist <= 512:
        return 7
    elif dist >= 513 and dist <= 1024:
        return 8
    elif dist >= 1025 and dist <= 2048:
        return 9
    elif dist >= 2049 and dist <= 4096:
        return 10
    elif dist >= 4097 and dist <= 8192:
        return 11
    elif dist >= 8193 and dist <= 16384:
        return 12
    elif dist >= 16385 and dist <= 32768:
        return 13

# Given a list of code lengths for a canonical Huffman tree,
# return the code length codes and associated extra bits- see deflate docs for length encoding scheme
def getcodelengthcodes(codelengths_list):
    
    prev = -1
    repeat_length = 0
    codelengthcodes = []
    repeat_extrabits = []
    for length in codelengths_list:

        #print("*\nprev: " + str(prev))
        #print("rptlen: " + str(repeat_length))

        # If the code length is a repeat, increase the repeat length
        # If we have reached the limit of repeat size, output code for repeat section
        if prev == length:
            repeat_length = repeat_length + 1
            if 1 <= prev <= 15 and repeat_length == 6:
                # Write repeat code (16) plus code for 6 repeats (3)
                codelengthcodes.append(16)
                repeat_extrabits.append(3)
                repeat_length = 0
            elif prev == 0 and repeat_length == 138:
                # Write long zero repeat code (18) plus code for 138 repeats (127)
                codelengthcodes.append(18)
                repeat_extrabits.append(127)
                repeat_length = 0

        # If we have changed code lengths, output code for last repeat section if
        # there is one, then output code for new character
        else:
            if repeat_length > 2:
                if prev == 0:
                    if 3 <= repeat_length <= 10:
                        codelengthcodes.append(17)
                        repeat_extrabits.append(repeat_length - 3)
                    elif 11 <= repeat_length <= 138:
                        codelengthcodes.append(18)
                        repeat_extrabits.append(repeat_length - 11)
                else:
                    if 3 <= repeat_length <= 6:
                        codelengthcodes.append(16)
                        repeat_extrabits.append(repeat_length - 3)

            if repeat_length == 1:
                codelengthcodes.append(prev)
            if repeat_length == 2:
                codelengthcodes.append(prev)
                codelengthcodes.append(prev)

            repeat_length = 0
            codelengthcodes.append(length)
            prev = length

        #print(length)
        #print(codelengthcodes)

    # Account for possible unprinted last repeat
    if not repeat_length == 0:
        if repeat_length > 2:
            if prev == 0:
                if 3 <= repeat_length <= 10:
                    codelengthcodes.append(17)
                    repeat_extrabits.append(repeat_length - 3)
                elif 11 <= repeat_length <= 138:
                    codelengthcodes.append(18)
                    repeat_extrabits.append(repeat_length - 11)
            else:
                if 3 <= repeat_length <= 6:
                    codelengthcodes.append(16)
                    repeat_extrabits.append(repeat_length - 3)

        if repeat_length == 1:
            codelengthcodes.append(prev)
        if repeat_length == 2:
            codelengthcodes.append(prev)
            codelengthcodes.append(prev)

    print(codelengthcodes)

    return((codelengthcodes, repeat_extrabits))

