# -*- coding: utf-8 -*-

"""

    0. Init
    
"""

# Import of libraries and initialization of file arguments.

import bitIO
import sys
import PQHeap
from Element import Element

infile = open(sys.argv[1], 'rb')
outfile = open(sys.argv[2], 'wb')

"""

    1. Scan input file and create frequency list of bytes in input file.
        
"""



# Add 256 empty Elements with a frequency of 0 to our frequency list table.

frequency_list = []

for i in range(256):
    frequency_list.append(Element(0,[i]))


# Open infile with Python IO and read the file byte for byte.
# Increase the frequency with 1 on the list index matching the byte decimal.

with infile as file:
    byte = file.read(1)
    while byte != b"":
        frequency_list[byte[0]].key = frequency_list[byte[0]].key + 1
        byte = file.read(1)

"""

    2. Run freq. list through the Huffman algorithm
    
"""

# PQHeap from Project part 2 is used to implement the Huffman algorithm.
# The Huffman algorithm extract the two smallest Element objects,
# merges them and inserts them as a new Element with the sum frequency
# in object.key and list elements in object.data.

def Huffman(Q):
    while len(Q) != 1:
            x = PQHeap.extractMin(Q)
            y = PQHeap.extractMin(Q)
            z = Element(x.key + y.key, [x.data, y.data]) 
            PQHeap.insert(Q,z)
    return Q
    
h_tree = Huffman(frequency_list.copy())

"""

    3. Convert Huffman tree to a table of passwords for each byte.

"""

# Using a recursive function the script searches through the Huffman tree
# to find leaves (which have a len() of 1) keeping a password in a string
# as it traverses through the tree. 

passw_table = [0] * 256

def genPassword(T):
    passw = ""
    root = T[0].data
    genPassword_func(root, passw)


def genPassword_func(T, passw):  
    if len(T) == 2:
        genPassword_func(T[0], passw+"0")
        genPassword_func(T[1], passw+"1")
    if len(T) == 1:
        passw_table[int(T[0])] = passw+"0"


genPassword(h_tree)

"""

    4. Write freq. list to output file in 32 bit.

"""

# The BitWriter writes the key of every item on the frequency list
# into the output file. 

bitstreamout = bitIO.BitWriter(outfile)

for i in range(256):
    bitstreamout.writeint32bits(frequency_list[i].key)


"""

    5. Rescan input file and match bytes to passwords,
    then write the passwords to the output file.

"""

# Reopen the file from the beginning.

infile = open(sys.argv[1], 'rb')

# Read the file byte for byte and then use BitWriters writebit() to write 
# the bits in the password to the output file.
# A range-based loop loops through the password one char at a time.

with infile as file:
    byte = file.read(1)
    while byte != b"":
        for i in range(len(passw_table[byte[0]])):
            if passw_table[byte[0]][i] == "0":
                bitstreamout.writebit(0)
            if passw_table[byte[0]][i] == "1":
                bitstreamout.writebit(1)
        byte = file.read(1)
    bitstreamout.close()


