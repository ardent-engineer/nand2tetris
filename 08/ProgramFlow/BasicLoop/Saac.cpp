#include <iostream>
using namespace std;
int factorial(int a);
int main (void)
{
    cout << factorial(5) << endl;
}
int factorial(int a)
{
    if (a==1)
    {
        return 1;
    }
    else
    {
        return a*factorial(a-1);
    }
}