#include "../hwlib/library/hwlib.hpp"

extern "C" void print(int x)
{
    hwlib::cout << x << "\n";
    return;
}
extern "C" void fibonacci();

int main (void)
{
    hwlib::wait_ms(2000); 
    hwlib::cout << "start AapNootMies\n";
    fibonacci();
    hwlib::cout << "end AapNootMies\n";
}
