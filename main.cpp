#include <iostream>

extern "C"
{
    void print(int x)
    {
        std::cout << x;
    }
}
