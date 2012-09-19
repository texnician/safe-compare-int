from itertools import *

def Unsigned(t):
    return 'unsigned {0}'.format(t)

BASE_INT_TYPES = ['char', 'int', 'long', 'long long']

UNSIGEND_INT_TYPES = imap(Unsigned, BASE_INT_TYPES)

def TypeCombinations(type_list):
    return permutations(type_list, 2)

def SameSignTypeCombinations():
    return chain(TypeCombinations(BASE_INT_TYPES), TypeCombinations(UNSIGEND_INT_TYPES))
