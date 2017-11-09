# huff_functions.py
# Contains functions for building huffman trees

import heapq as hq

# Build forest of nodes of form (frequency, index, left child, right child)
def build_forest(freqs):
    forest = []
    for node in freqs:
        hq.heappush(forest, ((freqs[node],node,None,None)))
    return forest

# Builds a huffman tree from a forest (heap)
def buildhufftree(forest):
    placeholder_index = -1
    while len(forest) > 1:
        node1 = hq.heappop(forest)
        node2 = hq.heappop(forest)
        hq.heappush(forest, (node1[0] + node2[0], placeholder_index, node1, node2))
        placeholder_index = placeholder_index - 1
    return(forest)

# Builds a huff table from a huffman tree
def buildhufftable(forest):
    huff_table = {}
    buildhufftable_rec(forest[0], "", huff_table)
    return huff_table

# Recursive helper method for building huff table
def buildhufftable_rec(node, cur_sequence, huff_table):
    if not node[2] and not node[3]:
        huff_table[node[1]] = cur_sequence
    else:
        buildhufftable_rec(node[2], cur_sequence + "0", huff_table)
        buildhufftable_rec(node[3], cur_sequence + "1", huff_table)
    
# Gets a list of code lengths from a huffman tree
def getcodelengths(tree):
    len_table = {}
    getcodelengths_rec(tree[0], 0, len_table)
    return len_table

# Recursive helper method for getting code lengths
def getcodelengths_rec(node, cur_length, len_table):
    if not node[2] and not node[3]:
        len_table[node[1]] = cur_length
    else:
        getcodelengths_rec(node[2], cur_length + 1, len_table)
        getcodelengths_rec(node[3], cur_length + 1, len_table)

# Given an ordered symbol set list and a dictionary of symbol/code length pairs,
# construct a list of code lengths w/same order as symbol set
def lengthslist(symbols, lengths):
    llist = []
    for symbol in symbols:
        if symbol in lengths:
            llist.append(lengths[symbol])
        else:
            llist.append(0)
    return llist
    
# Given an ordered symbol set list and a list of code lengths,
# constructs a dictionary containing the corresponding canonical huffman code
# Algorithm from DEFLATE docs
def makecanonical(symbols, lengths):

    max_length = 0
    for i in range(0, len(lengths)):
        if lengths[i] > max_length:
            max_length = lengths[i]

    bitlength_counts = []
    for i in range(0, max_length + 1):
        bitlength_counts.append(0)

    # Count number of codes with each bit length
    for i in range(0, len(lengths)):
        bitlength_counts[lengths[i]] = bitlength_counts[lengths[i]] + 1

    # Find numerical value of smallest code of each bit length &
    # store them in next_code
    bitlength_counts[0] = 0
    code = 0

    next_code = []
    next_code.append(0)
    for bits in range(1, max_length + 1):
        code = (code + bitlength_counts[bits-1]) << 1
        next_code.append(code)

    canon_codes = {}
    for i in range(0, len(symbols)):
        if lengths[i] != 0:
            canon_codes[symbols[i]] = next_code[lengths[i]]
            next_code[lengths[i]] = next_code[lengths[i]] + 1

    return canon_codes
    
