# huff_functions.py
# Contains functions for building huffman trees

import heapq as hq

# Build forest of nodes of form (frequency, index, left child, right child)
def build_forest(freqs):
    forest = []
    for node in freqs:
        hq.heappush(forest, ((freqs[node],node,None,None)))
    return forest

def buildhufftree(forest):
    placeholder_index = -1
    while len(forest) > 1:
        node1 = hq.heappop(forest)
        node2 = hq.heappop(forest)
        hq.heappush(forest, (node1[0] + node2[0], placeholder_index, node1, node2))
        placeholder_index = placeholder_index - 1
    return(forest)

def buildhufftable(forest):
    huff_table = {}
    buildhufftable_rec(forest[0], "", huff_table)
    return huff_table

def buildhufftable_rec(node, cur_sequence, huff_table):
    if not node[2] and not node[3]:
        huff_table[node[1]] = cur_sequence
    else:
        buildhufftable_rec(node[2], cur_sequence + "0", huff_table)
        buildhufftable_rec(node[3], cur_sequence + "1", huff_table)
    
