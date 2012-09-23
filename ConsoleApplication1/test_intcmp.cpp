#ifdef _MSC_VER
#include <assert.h>
#define ASSERT_TRUE(exp) assert((exp) == true)
#define ASSERT_FALSE(exp) assert((exp) == false)
#endif
#include "intcmp.h"

template<typename L, typename R>
bool t_t_t_t_t_t(L lhs, R rhs)
{
    return IntEq(lhs, rhs) && !IntGe
};

void RunTest()
{}
