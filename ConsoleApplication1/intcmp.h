#ifndef INTCMP_H_
#define INTCMP_H_

struct __true_type
{
    static const bool value = true;
};

struct __false_type
{
    static const bool value = false;
};

template<typename L, typename R>
struct __same_sign : public __false_type {};

template<>
struct __same_sign<int, int> : public __true_type {};

template<typename L, typename R>
struct __signed_unsigned : public __false_type {};

template<>
struct __signed_unsigned<int, unsigned int> : public __true_type {};

template<typename L, typename R, bool same_sign>
struct __IntCmp;

template<typename L, typename R, bool signed_unsigned>
struct __IntCmpDiffSign;

template<typename L, typename R>
struct __IntCmp<L, R, true>
{
    static inline int Cmp(L lhs, R rhs)
        {
            return lhs < rhs ? -1 : (rhs < lhs ? 1 : 0);
        }
};

template<typename L, typename R>
struct __IntCmpDiffSign<L, R, true>
{
    static inline int Cmp(L lhs, R rhs)
        {
            return lhs < 0 ? -1 : __IntCmp<L, R, __same_sign<L, R>::value>::Cmp((R)lhs, rhs);
        }
};

template<typename L, typename R>
struct __IntCmpDiffSign<L, R, false>
{
    static inline int Cmp(L lhs, R rhs)
        {
            return __IntCmpDiffSign<R, L, __signed_unsigned<R, L>::value>::Cmp(rhs, lhs) * -1;
        }
};

template<typename L, typename R>
struct __IntCmp<L, R, false>
{
    static inline int Cmp(L lhs, R rhs)
        {
            return __IntCmpDiffSign<L, R, __signed_unsigned<L, R>::value>::Cmp(lhs, rhs);
        }
};

template<typename L, typename R>
inline int IntCmp(L lhs, R rhs)
{
    return __IntCmp<L, R, __same_sign<L, R>::value>::Cmp(lhs, rhs);
}

#endif  // INTCMP_H_
