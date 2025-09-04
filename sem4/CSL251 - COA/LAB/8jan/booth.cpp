#include <iostream>
#include<bits/stdc++.h>
using namespace std;

void complement(vector<int> &a){
    int n = a.size();
    for(int i = 0 ; i < n ; i++){
        a[i] = (a[i] + 1) % 2;
    }
    if(a[n - 1] == 0){
        a[n - 1] = 1;
        return;
    }else{
        a[n - 1] = 0;
        for(int i = n - 2 ; i >= 0 ; i--){
            if(a[i] == 0){
                a[i] = 1;
                return;
            }else{
                a[i] = 0;
            }
        }
    }
}

void addBinary(vector<int> &a, vector<int> &b) {
    int carry = 0;
    for (int i = a.size() - 1; i >= 0; i--) {
        int sum = a[i] + b[i] + carry;
        a[i] = sum % 2;
        carry = sum / 2;
    }
}

void arithmeticShiftRight(vector<int> &a, vector<int> &q, int &q_1) {
    q_1 = q.back();
    for (int i = q.size() - 1; i > 0; i--) {
        q[i] = q[i - 1];
    }
    q[0] = a.back();
    for (int i = a.size() - 1; i > 0; i--) {
        a[i] = a[i - 1];
    }
}

int binaryToDecimal(const vector<int> &binary) {
    int decimal = 0;
    int base = 1;
    for (int i = binary.size() - 1; i >= 0; i--) {
        decimal += binary[i] * base;
        base *= 2;
    }
    return decimal;
}

void boothAlgorithm(vector<int> &m, vector<int> &q) {
    int n = m.size();
    vector<int> a(n, 0);
    int q_1 = 0;

    vector<int> m_neg = m;
    complement(m_neg);

    for (int i = 0; i < n; i++) {
        if (q.back() == 1 && q_1 == 0) {
            addBinary(a, m_neg);
        } else if (q.back() == 0 && q_1 == 1) {
            addBinary(a, m);
        }
        arithmeticShiftRight(a, q, q_1);
    }

    cout << "Product (binary): ";
    for (int i = 0; i < n; i++) {
        cout << a[i];
    }
    for (int i = 0; i < n; i++) {
        cout << q[i];
    }
    cout << endl;

    vector<int> product;
    product.insert(product.end(), a.begin(), a.end());
    product.insert(product.end(), q.begin(), q.end());

    int decimalProduct = binaryToDecimal(product);
    cout << "Product (decimal): " << decimalProduct << endl;
}

int main() {

    int n;
    string a , b;
    cout<<"Enter the number of bits in the code word: ";
    cin >> n;
    cout<<"Enter the binary integer a : ";
    cin >> a;
    cout<<"Enter the binary integer b : ";
    cin >> b;
    vector<int> a1(n) , b1(n);
    for(int i = 0 ; i < n ; i++){
        a1[i] = a[i] - '0';
        b1[i] = b[i] - '0';
    }
    //here m = a1
    complement(a1);
    vector<int> shift;
    shift.push_back(0);
    for(int i = n - 2; i >= 1 ; i--){
        if(b1[i] != b[i + 1]){
            shift.push_back(n - i - 1);
        }
    }
    vector<vector<int>> ans;
    
    boothAlgorithm(a1, b1);

    return 0;
}