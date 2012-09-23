from itertools import *
import random

def RandLt(cls, val):
    return random.randrange(cls.min, min(val, cls.max)) if cls.min < val else None

def RandGt(cls, val):
    return random.randint(max(cls.min, val + 1), cls.max) if cls.max > val else None

def InRange(cls, val):
    return val >= cls.min and val <= cls.max

def GetEq(cls, val):
    return val if InRange(cls, val) else None

def RhsMap(cls, lhs):
    ret = {}
    ret['<'] = RandLt(cls, lhs)
    ret['>'] = RandGt(cls, lhs)
    ret['='] = GetEq(cls, lhs)
    return ret

class I8(object):
    ctp = 'char'
    min = -pow(2, 7)
    max = pow(2, 7) - 1

    @classmethod
    def Literal(cls, val):
        return '(char){0}'.format(val)

    @classmethod
    def RandSeq(cls):
        return [cls.min, random.randrange(cls.min + 1, 0), 0, random.randrange(cls.max/2, cls.max), cls.max]

class UI8(object):
    ctp = 'unsigned char'
    min = 0
    max = pow(2, 8) - 1

    @classmethod
    def Literal(cls, val):
        return '({0}){1}'.format(cls.ctp, val)

    @classmethod
    def RandSeq(cls):
        return [cls.min, random.randrange(cls.max / 2, cls.max), cls.max]

class I16(object):
    ctp = 'short'
    min = -pow(2, 15)
    max = pow(2, 15) - 1

    @classmethod
    def Literal(cls, val):
        return '(short){0}'.format(val)

    @classmethod
    def RandSeq(cls):
        return [cls.min,
                random.randrange(cls.min + 1, -pow(2, 7)),
                -pow(2, 7),
                random.randrange(-pow(2, 7)+1, 0),
                0,
                random.randrange(1, pow(2, 7) - 1),
                pow(2, 7) - 1,
                random.randrange(pow(2, 7), pow(2, 8) - 1),
                pow(2, 8) - 1,
                random.randrange(pow(2, 8), cls.max),
                cls.max]

class UI16(object):
    ctp = 'unsigned short'
    min = 0
    max = pow(2, 16) - 1

    @classmethod
    def Literal(cls, val):
        return '({0}){1}'.format(cls.ctp, val)

    @classmethod
    def RandSeq(cls):
        return [cls.min,
                random.randrange(1, pow(2, 7) - 1),
                pow(2, 7) - 1,
                random.randrange(pow(2, 7), pow(2, 8) - 1),
                pow(2, 8) - 1,
                random.randrange(pow(2, 8), cls.max),
                cls.max]
                
INT_TYPES = [I8, UI8, I16, UI16]

def IntEq(lhs, rhs):
    return lhs == rhs

def IntNe(lhs, rhs):
    return lhs != rhs

def IntLt(lhs, rhs):
    return lhs < rhs

def IntLe(lhs, rhs):
    return lhs <= rhs

def IntGt(lhs, rhs):
    return lhs > rhs

def IntGe(lhs, rhs):
    return lhs >= rhs

OPS = [IntEq, IntNe, IntLt, IntLe, IntGt, IntGe]

def GenTestCase(ltp, lhs, rtp, rhs):
    def fn(f):
        result = f(lhs, rhs)
        exp = 'ASSERT_TRUE' if result else 'ASSERT_FALSE'
        return '{0}({1}({2}, {3}));'.format(exp, f.__name__, ltp.Literal(lhs), rtp.Literal(rhs))
    return [ fn(f) for f in OPS ]

def TypeCombinations(type_list):
    return permutations(type_list, 2)

def ZipRhsMap(lhs, rhs_map):
    return zip(repeat(lhs), [rhs for rhs in rhs_map.itervalues() if rhs is not None])

def ValueCombine(tp1, tp2):
    return list(chain(*(ZipRhsMap(lhs, RhsMap(tp2, lhs)) for lhs in tp1.RandSeq())))

def TestList(types):
    return [[x, y, ValueCombine(x, y)] for x, y in TypeCombinations(types)]

def TestCase(types):
    result = []
    for ltp, rtp, cases in TestList(types):
        result.append('// {0} vs {1}'.format(ltp.ctp, rtp.ctp))
        for lhs, rhs in cases:
            result.extend(GenTestCase(ltp, lhs, rtp, rhs))
    return result

def GenCpp(types):
    with open('test_intcmp.cpp', 'w') as of:
        of.write('#ifdef _MSC_VER\n')
        of.write('#include <assert.h>\n')
        of.write('#define ASSERT_TRUE(exp) assert((exp) == true)\n')
        of.write('#define ASSERT_FALSE(exp) assert((exp) == false)\n')
        of.write('#endif\n')
        of.write('#include "intcmp.h"\n')
        of.write('void RunTest()\n')
        of.write('{\n')
        of.write('\n'.join(TestCase(INT_TYPES)))
        of.write('}\n')

if __name__ == '__main__':
    GenCpp(INT_TYPES)
