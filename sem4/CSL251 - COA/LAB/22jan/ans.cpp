#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

int AddSub(int A, int B, bool isSub, int n)
{
    if (isSub)
    {
        B = ~B + 1;
    }
    int sum = A + B;
    int mask = (1 << n) - 1; // Mask is to set limit to n bits so that overflow is handled
    sum &= mask;
    return sum;
}

void UnsignedBinaryDivision(int Q, int M, int n)
{
    int A = 0;
    int Count = n;
    int mask = (1 << n) - 1; // Mask is to set limit to n bits so that overflow is handled

    cout << "Initial Values: A = " << A << ", Q = " << Q << endl;

    while (Count > 0)
    {
        A = (A << 1) | ((Q >> (n - 1)) & 1);
        Q = (Q << 1) & mask;

        A = AddSub(A, M, true, n);

        if ((A & (1 << (n - 1))) != 0)
        {
            A = AddSub(A, M, false, n);
            Q &= ~(1);
        }
        else
        {
            Q |= 1;
        }

        Count--;

        cout << "Step: A = " << A << ", Q = " << Q << ", Count = " << Count << endl;
    }

    cout << "Final Values: Quotient (Q) = " << Q << ", Remainder (A) = " << A << endl;
}

int main()
{
    int Q, M, n;
    cout << "Enter the dividend (Q): ";
    cin >> Q;
    cout << "Enter the divisor (M): ";
    cin >> M;
    cout << "Enter the number of bits (n): ";
    cin >> n;

    if (Q < 0 || M <= 0 || n <= 0)
    {
        cout << "Invalid input! Ensure Q >= 0, M > 0, and n > 0." << endl;
        return 1;
    }

    cout << "Performing Unsigned Binary Division for Q = " << Q << ", M = " << M << ", n = " << n << endl;
    UnsignedBinaryDivision(Q, M, n);

    return 0;
}
