# -*- coding: utf-8 -*-

# Import of libraries and initialization of file arguments.

import bitIO
import sys
import PQHeap
from Element import Element

infile = open(sys.argv[1], 'rb')
outfile = open(sys.argv[2], 'wb')

bitstreamin = bitIO.BitReader(infile)

"""

    1. Read frequency table from input file.
    
"""

# Reads 256 32 bit ints from the encoded input file using BitWriters 
# readint32bits() and recreates the frequency list.

frequency_list = []


for i in range(256):
    x = bitstreamin.readint32bits()
    frequency_list.append(Element(x,[i]))
    
"""

    2. Generate Huffman tree
    
"""

# Uses the same code from Encode.py to build the exact same Huffman tree

def Huffman(Q):
    while len(Q) != 1:
            x = PQHeap.extractMin(Q)
            y = PQHeap.extractMin(Q)
            z = Element(x.key + y.key, [x.data, y.data]) 
            PQHeap.insert(Q,z)
    return Q
    
h_tree = Huffman(frequency_list.copy())

    
"""

    3. Decode file
    
"""

# findBytes() reads one bit from the encoded input file and uses it to navigate 
# the Huffman tree. The length of the list indicates whether it is a node 
# or a leaf. If it is not a leaf (len() = 1), the function reads another bit 
# and continues down the tree. When a leaf is found a byte is written 
# to the output file, and the function gets reset to start at the root.
# The function runs until it has found the same amount of bytes
# as the root frequency of the Huffman tree.

def findBytes(T):
    root = T[0].data
    position = root
    bytes_found = 0
    
    while bytes_found < T[0].key:
        readBit = bitstreamin.readbit()
        if position == None:
            position = root
            bytes_found += 1
        position = findBytes_func(position, readBit)

# Navigates the tree using the length of the elements (nodes). When 2, it will
# continue to the next element. When 1, it has found a leaf and will write the
# byte to the output file.
# Return "None" makes sure that findBytes() start from the root again.

def findBytes_func(node, bit):    
    if len(node) == 2:
        return node[int(bit)]
    if len(node) == 1:
        byte = node[0]
        outfile.write(bytes([byte]))
        return None
        

findBytes(h_tree)

# Closes the BitWriter to pad the output with 0-bits to get a full number of bytes.

bitstreamin.close()