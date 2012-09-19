// ConsoleApplication1.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <memory>
#include <string>
#include "intcmp.h"

int _tmain(int argc, _TCHAR* argv[])
{
	std::shared_ptr<int> p(new int(8));
    if (p)
    {
        ++*p;
    }
	std::unique_ptr<std::string> us(new std::string("abc"));
	printf("%d\n", *p);
	printf("%s\n", us->c_str());
    printf("%d\n", IntCmp(1, 2));
    printf("%d\n", IntCmp(2, 1));
    printf("%d\n", IntCmp(2, 2));
    int n = -1;
    printf("%d\n", n < (unsigned int)1);
    printf("%d\n", n < (int)1);
	return 0;
}
