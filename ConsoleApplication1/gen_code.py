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

class I32(object):
    ctp = 'int'
    min = -pow(2, 31)
    max = pow(2, 31) - 1

    @classmethod
    def Literal(cls, val):
        return '{0}({1})'.format(cls.ctp, val)

    @classmethod
    def RandSeq(cls):
        return list(chain([cls.min,
                           random.randrange(cls.min + 1, I16.min)],
                          I16.RandSeq(),
                          [random.randrange(I16.max+1, cls.max),
                           cls.max]))
class UI32(object):
    ctp = 'unsigned int'
    min = 0
    max = pow(2, 32) - 1

    @classmethod
    def Literal(cls, val):
        return '({0})({1}U)'.format(cls.ctp, val)

    @classmethod
    def RandSeq(cls):
        return list(chain(UI16.RandSeq(),
                          [random.randrange(UI16.max + 1, cls.max),
                           cls.max]))

class I64(object):
    ctp = 'long long'
    min = -pow(2, 63)
    max = pow(2, 63) - 1

    @classmethod
    def Literal(cls, val):
        return '({0})({1}LL)'.format(cls.ctp, val)

    @classmethod
    def RandSeq(cls):
        return list(chain([cls.min,
                           random.randrange(cls.min + 1, I32.min)],
                          I32.RandSeq(),
                          [random.randrange(I32.max + 1, cls.max),
                           cls.max]))

class UI64(object):
    ctp = 'unsigned long long'
    min = 0
    max = pow(2, 64) - 1

    @classmethod
    def Literal(cls, val):
        return '({0})({1}ULL)'.format(cls.ctp, val)

    @classmethod
    def RandSeq(cls):
        return list(chain(UI32.RandSeq(),
                          [random.randrange(UI32.max + 1, cls.max),
                           cls.max]))

class L32(object):
    ctp = 'long'
    min = I32.min
    max = I32.max

    @classmethod
    def Literal(cls, val):
        return '({0})({1}L)'.format(cls.ctp, val)

    @classmethod
    def RandSeq(cls):
        return I32.RandSeq()

class UL32(object):
    ctp = 'unsigned long'
    min = UI32.min
    max = UI32.max

    @classmethod
    def Literal(cls, val):
        return '({0})({1}UL)'.format(cls.ctp, val)

    @classmethod
    def RandSeq(cls):
        return UI32.RandSeq()

INT_TYPES = [I8, UI8, I16, UI16, I32, UI32, L32, UL32, I64, UI64]

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

def GenShortTestCase(ltp, lhs, rtp, rhs):
    return ['{0}_{1}_{2}_{3}_{4}_{5}({6}, {7});'.format(*chain(('T' if f(lhs, rhs) else 'F' for f in OPS),
                                                               (ltp.Literal(lhs), rtp.Literal(rhs),)))]

def TypeCombinations(type_list):
    return permutations(type_list, 2)

def ZipRhsMap(lhs, rhs_map):
    return zip(repeat(lhs), [rhs for rhs in rhs_map.itervalues() if rhs is not None])

def ValueCombine(tp1, tp2):
    return list(chain(*(ZipRhsMap(lhs, RhsMap(tp2, lhs)) for lhs in tp1.RandSeq())))

def TestList(types):
    return [[x, y, ValueCombine(x, y)] for x, y in TypeCombinations(types)]

def PredPermutations(n):
    if n == 1:
        return [[True], [False]]
    else:
        sub = PredPermutations(n - 1)
        return list(chain(map(lambda x: list(chain([True], x)), sub),
                          map(lambda x: list(chain([False], x)), sub)))

def FilterPredPermutations(preds):
    def by_eq(f):
        def fn(p):
            eq = p[0]
            if eq:
                return f(p) and not p[1] and not p[2] and p[3] and not p[4] and p[5]
            else:
                return f(p) and p[1]
        return fn
    def by_ne(f):
        def fn(p):
            ne = p[1]
            if ne:
                return f(p) and not p[0]
            else:
                return f(p) and p[0] and not p[2] and p[3] and not p[4] and p[5]
        return fn
    def by_lt(f):
        def fn(p):
            lt = p[2]
            if lt:
                return f(p) and not p[0] and p[1] and p[3] and not p[4] and not p[5]
            else:
                return f(p) and p[5]
        return fn
    def by_le_ge(f):
        def fn(p):
            le = p[3]
            ge = p[5]
            if le and ge:
                return f(p) and p[0] and not p[1] and not p[2] and not p[4]
            elif le:
                return f(p) and p[2] and not p[4]
            elif ge:
                return f(p) and not p[2] and p[4]
            else:
                return False
        return fn
    return filter(by_eq(by_le_ge(by_lt(by_ne(lambda x: True)))), preds)

def GenPredCombination(pred):
    def fn(p, f):
        return '{0}{1}((lhs), (rhs))'.format('' if p else '!', f.__name__)
    return '''#define {0}_{1}_{2}_{3}_{4}_{5}(lhs, rhs) ASSERT_TRUE(({6} && {7} && {8} && {9} && {10} && {11}))'''.format(*chain(( 'T' if x else 'F' for x in pred),
                                                                                                                                 ( fn(p, f) for p, f in izip(pred, OPS))))
def TestCase(types):
    result = []
    for ltp, rtp, cases in TestList(types):
        result.append('// {0} vs {1}'.format(ltp.ctp, rtp.ctp))
        for lhs, rhs in cases:
            result.extend(GenShortTestCase(ltp, lhs, rtp, rhs))
    return result

def GenCpp(types):
    with open('test_intcmp.cpp', 'w') as of:
        of.write('#ifdef _MSC_VER\n')
        of.write('#include <assert.h>\n')
        of.write('#define ASSERT_TRUE(exp) assert((exp) == true)\n')
        of.write('#define ASSERT_FALSE(exp) assert((exp) == false)\n')
        of.write('#endif\n')
        of.write('#include "intcmp.h"\n')
        of.write('\n')
        of.write('\n'.join((GenPredCombination(x) for x in FilterPredPermutations(PredPermutations(6)))))
        of.write('\n')
        of.write('\n')
        of.write('void RunTest()\n')
        of.write('{\n')
        of.write('\n'.join(('  {0}'.format(x) for x in TestCase(INT_TYPES))))
        of.write('}\n')

if __name__ == '__main__':
    GenCpp(INT_TYPES)
