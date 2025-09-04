#include <iostream>
#include <cmath>
#include <limits>
#include <iomanip>
using namespace std;

double getSignificand(const string &S)
{
    double significand = 1.0;
    for (size_t i = 0; i < S.size(); i++)
    {
        if (S[i] == "1"[0])
        {
            significand += pow(2, -(i + 1));
        }
    }
    return significand;
}

bool isValidBinary(const string &S)
{
    for (char c : S)
    {
        if (c != '0' && c != '1')
        {
            return false;
        }
    }
    return true;
}

void floatingPointOperation(int n, int m, string S1, string S2, string E1, string E2, bool isAddition)
{
    if (!isValidBinary(S1) || !isValidBinary(S2) || !isValidBinary(E1) || !isValidBinary(E2))
    {
        cout << "Error: Invalid binary input." << endl;
        return;
    }

    int exp1 = stoi(E1, nullptr, 2);
    int exp2 = stoi(E2, nullptr, 2);

    double significand1 = getSignificand(S1);
    double significand2 = getSignificand(S2);

    if (!isAddition)
    {
        significand2 = -significand2;
    }

    if (exp1 > exp2)
    {
        significand2 /= (1 << (exp1 - exp2));
        exp2 = exp1;
    }
    else if (exp2 > exp1)
    {
        significand1 /= (1 << (exp2 - exp1));
        exp1 = exp2;
    }

    double resultSignificand = significand1 + significand2;
    int resultExponent = exp1;

    if (resultSignificand == 0.0)
    {
        cout << "Result: 0" << endl;
        return;
    }

    while (resultSignificand >= 2.0)
    {
        resultSignificand /= 2.0;
        resultExponent++;
    }
    while (resultSignificand < 1.0)
    {
        if (resultExponent == -(1 << (m - 1)))
        {
            cout << "Error: Exponent underflow." << endl;
            return;
        }
        resultSignificand *= 2.0;
        resultExponent--;
    }

    if (resultExponent > (1 << (m - 1)) - 1)
    {
        cout << "Error: Exponent overflow." << endl;
        return;
    }

    cout << "Result: " << scientific << resultSignificand << " x 2^" << resultExponent << endl;
}

int main()
{
    int n, m;
    string S1, S2, E1, E2;
    bool isAddition;

    cout << "Enter n (bit length of significand): ";
    cin >> n;
    cout << "Enter m (bit length of exponent): ";
    cin >> m;
    cout << "Enter significand S1: ";
    cin >> S1;
    cout << "Enter exponent E1: ";
    cin >> E1;
    cout << "Enter significand S2: ";
    cin >> S2;
    cout << "Enter exponent E2: ";
    cin >> E2;
    cout << "Enter operation (1 for addition, 0 for subtraction): ";
    cin >> isAddition;

    floatingPointOperation(n, m, S1, S2, E1, E2, isAddition);
    return 0;
}
