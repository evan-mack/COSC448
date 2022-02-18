from suffixtree import *


stree = SuffixTree('ACATGATTACAATCGCGTATTATACGGA')

print(stree.hasSubstring('GATTACA')) #True

print(stree.hasSuffix('GATTACA')) #False

print(stree.hasSuffix('TACGGA')) #True

stree.printTree()