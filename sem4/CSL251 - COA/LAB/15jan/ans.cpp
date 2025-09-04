#include <iostream>
#include <bitset>
using namespace std;

// for negative numbers, sign extend the number to n bits
int SignExtend(int num, int n) {
    if (num & (1 << (n-1))) {
        num |= (~0 << n);
    }
    return num;
}

int AddSub(int A, int B, int n) {
    int result = A + B;
    int mask = (1 << n) - 1; // this ensures that the result is n bits
    result &= mask;
    return SignExtend(result, n);
}

void BoothAlgorithm(int multiplicand, int multiplier, int n) {
    int A = 0;
    int Q = SignExtend(multiplier & ((1 << n) - 1), n);
    int M = SignExtend(multiplicand & ((1 << n) - 1), n);
    int Q_1 = 0;
    int Count = n;

    cout << "\nMultiplicand (M): " << M << " (" << bitset<8>(M) << ")" << endl;
    cout << "Multiplier (Q): " << Q << " (" << bitset<8>(Q) << ")" << endl;
    cout << "\nStep\tA\t\tQ\tQ_1\n";
    cout << "Init\t" << bitset<8>(A) << "\t" << bitset<8>(Q) << "\t" << Q_1 << endl;

    while (Count > 0) {
        // Check last two bits (Q0Q-1)
        int Q0 = Q & 1;
        
        if (Q0 == 1 && Q_1 == 0) {
            A = AddSub(A, -M, n);
        } else if (Q0 == 0 && Q_1 == 1) {
            A = AddSub(A, M, n);
        }

        // Arithmetic right shift
        Q_1 = Q & 1;
        int lsb_A = A & 1;
        Q = (Q >> 1) | ((lsb_A) << (n-1));
        
        // Sign extension for A
        if (A & (1 << (n-1))) {
            A = ((A >> 1) | (1 << (n-1))) & ((1 << n) - 1);
        } else {
            A = (A >> 1) & ((1 << n) - 1);
        }

        Count--;
        cout << Count << "\t" << bitset<8>(A) << "\t" << bitset<8>(Q) << "\t" << Q_1 << endl;
    }

    // Calculate final result considering sign
    int result = ((A & ((1 << n) - 1)) << n) | (Q & ((1 << n) - 1));
    result = SignExtend(result, 2*n);
    
    cout << "\nFinal Result: " << result << endl;
    cout << "Binary: " << bitset<16>(result) << endl;
}

int main() {
    int n, multiplicand, multiplier;

    cout << "Enter the number of bits (n): ";
    cin >> n;

    cout << "Enter the multiplicand (in decimal): ";
    cin >> multiplicand;

    cout << "Enter the multiplier (in decimal): ";
    cin >> multiplier;

    BoothAlgorithm(multiplicand, multiplier, n);

    return 0;
}