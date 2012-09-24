#ifndef INTCMP_H_
#define INTCMP_H_

namespace ambition
{
namespace internal
{
struct true_type
{
  static const bool value = true;
};

struct false_type
{
  static const bool value = false;
};

template<typename T>
struct signed_int : public true_type
{};

template<>
struct signed_int<unsigned char> : public false_type
{};

template<>
struct signed_int<unsigned short> : public false_type
{};

template<>
struct signed_int<unsigned int> : public false_type
{};

template<>
struct signed_int<unsigned long> : public false_type
{};

template<>
struct signed_int<unsigned long long> : public false_type
{};

template<typename T>
struct safe_unsigned_cast
{
    typedef T type;
};

template<>
struct safe_unsigned_cast<char>
{
    typedef unsigned char type;
};

template<>
struct safe_unsigned_cast<short>
{
    typedef unsigned short type;
};

template<>
struct safe_unsigned_cast<int>
{
    typedef unsigned int type;
};

template<>
struct safe_unsigned_cast<long>
{
    typedef unsigned long type;
};

template<>
struct safe_unsigned_cast<long long>
{
    typedef unsigned long long type;
};

template<typename L, bool lsigned, typename R, bool rsigned>
struct SafeIntCmp
{
  // default implementation for same sign
  static inline int Cmp(L lhs, R rhs)
    {
      return lhs < rhs ? -1 : (rhs < lhs ? 1 : 0);
    }
  static inline bool Eq(L lhs, R rhs)
    {
      return lhs == rhs;
    }
  static inline bool Ne(L lhs, R rhs)
    {
      return lhs != rhs;
    }
  static inline bool Lt(L lhs, R rhs)
    {
      return lhs < rhs;
    }
  static inline bool LtEq(L lhs, R rhs)
    {
      return lhs <= rhs;
    }
};

template<typename L, typename R>
struct SafeIntCmp<L, true, R, false>
{
  typedef typename safe_unsigned_cast<L>::type UL;

  static inline int Cmp(L lhs, R rhs)
    {
      return (lhs < 0) ? -1 : SafeIntCmp<UL, signed_int<UL>::value, R, signed_int<R>::value>::Cmp((UL)lhs, rhs);
    }
  static inline bool Eq(L lhs, R rhs)
    {
      return (lhs < 0) ? false : SafeIntCmp<UL, signed_int<UL>::value, R, signed_int<R>::value>::Eq((UL)lhs, rhs);
    }
  static inline bool Ne(L lhs, R rhs)
    {
      return (lhs < 0) ? true : SafeIntCmp<UL, signed_int<UL>::value, R, signed_int<R>::value>::Ne((UL)lhs, rhs);
    }
  static inline bool Lt(L lhs, R rhs)
    {
      return (lhs < 0) ? true : SafeIntCmp<UL, signed_int<UL>::value, R, signed_int<R>::value>::Lt((UL)lhs, rhs);
    }
  static inline bool LtEq(L lhs, R rhs)
    {
      return (lhs < 0) ? true : SafeIntCmp<UL, signed_int<UL>::value, R, signed_int<R>::value>::LtEq((UL)lhs, rhs);
    }
};

template<typename L, typename R>
struct SafeIntCmp<L, false, R, true>
{
  typedef typename safe_unsigned_cast<R>::type UR;
  
  // unsigned cmp signed
  static inline int Cmp(L lhs, R rhs)
    {
      return -1 * SafeIntCmp<R, signed_int<R>::value, L, signed_int<L>::value>::Cmp(rhs, lhs);
    }
  static inline bool Eq(L lhs, R rhs)
    {
      return SafeIntCmp<R, signed_int<R>::value, L, signed_int<L>::value>::Eq(rhs, lhs);
    }
  static inline bool Ne(L lhs, R rhs)
    {
      return SafeIntCmp<R, signed_int<R>::value, L, signed_int<L>::value>::Ne(rhs, lhs);
    }
  static inline bool Lt(L lhs, R rhs)
    {
      return (rhs < 0) ? false : SafeIntCmp<L, signed_int<L>::value, UR, signed_int<UR>::value>::Lt(lhs, rhs);
    }
  static inline bool LtEq(L lhs, R rhs)
    {
      return (rhs < 0) ? false : SafeIntCmp<L, signed_int<L>::value, UR, signed_int<UR>::value>::LtEq(lhs, rhs);
    }
};

} // namespace internal
} // namespace ambition

template<typename L, typename R>
inline int IntCmp(L lhs, R rhs)
{
  using namespace ::ambition;
  return internal::SafeIntCmp<L, internal::signed_int<L>::value, R, internal::signed_int<R>::value>::Cmp(lhs, rhs);
}

template<typename L, typename R>
inline bool IntEq(L lhs, R rhs)
{
  using namespace ::ambition;
  return internal::SafeIntCmp<L, internal::signed_int<L>::value, R, internal::signed_int<R>::value>::Eq(lhs, rhs);
}

template<typename L, typename R>
inline bool IntNe(L lhs, R rhs)
{
  using namespace ::ambition;
  return internal::SafeIntCmp<L, internal::signed_int<L>::value, R, internal::signed_int<R>::value>::Ne(lhs, rhs);
}

template<typename L, typename R>
inline bool IntLt(L lhs, R rhs)
{
  using namespace ::ambition;
  return internal::SafeIntCmp<L, internal::signed_int<L>::value, R, internal::signed_int<R>::value>::Lt(lhs, rhs);
}

template<typename L, typename R>
inline bool IntLtEq(L lhs, R rhs)
{
  using namespace ::ambition;
  return internal::SafeIntCmp<L, internal::signed_int<L>::value, R, internal::signed_int<R>::value>::LtEq(lhs, rhs);
}

#define IntLe(a, b) (IntLtEq((a), (b))) // a <= b
#define IntGt(a, b) (IntCmp((a), (b)) > 0) // a > b
#define IntGe(a, b) (IntCmp((a), (b)) >= 0) // a >= b

#endif  // INTCMP_H_
