#include<iostream>
#include<fstream>
#include<string>
#include<cstring>
using namespace std;

void Swap(int &a, int &b)
{
    int temp = a;
    a = b;
    b = temp;
}

void heapify(int arr[], int n, int i)
{
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    if (left < n && arr[left] > arr[largest])
    {
        largest = left;
    }
    if (right < n && arr[right] > arr[largest])
    {
        largest = right;
    }
    if (largest != i)
    {
        Swap(arr[largest], arr[i]);
        heapify(arr, n, largest);
    }
}

void print(int arr[], int n)
{
    for (int i = 0; i < n; i++)
    {
        cout << arr[i] << " ";
    }
    cout << endl;
}

int main(){

    string file;
    string line1,line2;
    int n;
    int * a;
    cout<<"Enter file name : ";
    cin>>file;

    ifstream F(file);

    if(F.is_open()){
        getline(F,line1);
        //cout<<line1<<endl;
        getline(F,line2);
        //cout<<line2<<endl;
        F.close();
    }else{
        cout<<"Error opening file."<<endl;
    }
    n = stoi(line1);
    a = new int[n];
    int i = 0;
    char * token = strtok(line2, " ");
    while (token != nullptr) {
        a[i++] = atoi(token);
        token = strtok(nullptr, " ");   
    }
    cout<<n<<endl<<endl;
    print(a,n);



    return 0;
}