# DEFLATE_FNS.py
# Handy helper functions for DEFLATE.

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

