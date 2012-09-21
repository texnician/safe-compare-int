from itertools import *
import random

def RandLt(cls, val):
    return random.randrange(cls.min, min(val, cls.max)) if cls.min < val else None

def RandGt(cls, val):
    return random.randint(max(cls.min, val + 1), cls.max) if cls.max > val else None

def InRange(cls, val):
    return val >= cls.min and val <= cls.max

def GetEq(cls, val):
    return val if cls.InRange(val) else None

class I8(object):
    ctp = 'char'
    min = -pow(2, 7)
    max = pow(2, 7) - 1

    @classmethod
    def Literal(cls, val):
        return str(val)

    @classmethod
    def RandSeq(cls):
        return [random.randrange(cls.min, 0), 0, random.randint(cls.max/2, cls.max)]

    @classmethod
    def InRange(cls, val):
        return val >= cls.min and val <= cls.max

    @classmethod
    def RhsMap(cls, lhs):
        ret = {}
        ret['<'] = RandLt(cls, lhs)
        ret['>'] = RandGt(cls, lhs)
        ret['='] = GetEq(cls, lhs)
        return ret

print I8.RhsMap(-9999)
print I8.RhsMap(-3)
print I8.RhsMap(0)
print I8.RhsMap(127)
print I8.RhsMap(128)
print I8.RhsMap(9999)

def TypeCombinations(type_list):
    return permutations(type_list, 2)

def SameSignTypeCombinations():
    return chain(TypeCombinations(BASE_INT_TYPES), TypeCombinations(UNSIGEND_INT_TYPES))
