#include<iostream>
#include<chrono>
using namespace std;
using std::chrono::high_resolution_clock;
using std::chrono::duration;

void printArray(int *arr, int size)
{
    for (int i = 0; i < size; i++)
        cout << arr[i] << " ";
    cout << endl;
}

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

// bubble sort
void b_sort(int a[], int n)
{
    for (int i = 0; i < n; i++)
    {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++)
        {
            if (a[j] > a[j + 1])
            {
                swap(&a[j], &a[j + 1]);
                swapped = true;
            }
        }
        if (swapped == false)
        {
            break;
        }
    }
}

// insertion sort
void i_sort(int a[], int n)
{
    /* for(int i=1;i<n;i++)
    {
        int temp = a[i];
        int j=i-1;
        for(;j>=0;j--)
        {
            if(a[j]>temp)
            {
                a[j+1]=a[j];
            }
            else{
                break;
            }
            a[j]=temp;
        }

    } */

    /*    for(int i=1;i<n;i++)
       {
            int temp=a[i];
            int j=i-1;
            while(j>=0)
            {
                if (a[j]>temp)
                {
                    a[j+1]=a[j];
                }
                else{
                    break;
                }
                a[j]=temp;
                j--;
            }
       } */

    int i = 1;
    while (i < n)
    {
        int temp = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > temp)
        {
            a[j + 1] = a[j];
            a[j] = temp;
            j--;
        }
        i++;
    }
}

//heapSort
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
        swap(arr[largest], arr[i]);
        heapify(arr, n, largest);
    }
}

void heapSort(int a[],int n){

    for (int i = n / 2 -1; i >= 0; i--){
        heapify(a,n,i);
    }
    for(int i = n - 1; i >= 0; i--){
        swap(a[0],a[i]);
        heapify(a,i,0);
    }

}


// merge sort

// merging
void merge(int *arr, int s, int e)
{
    int mid = s + (e - s) / 2;
    int len1 = mid - s + 1;
    int len2 = e - mid;

    int *firstPart = new int[len1];
    int *secondPart = new int[len2];

    // copying data
    int l = s;
    // left part
    for (int i = 0; i < len1; i++)
    {
        firstPart[i] = arr[l];
        l++;
    }
    // right part
    int r = mid + 1;
    for (int i = 0; i < len2; i++)
    {
        secondPart[i] = arr[r];
        r++;
    }

    // merging

    int index1 = 0;
    int index2 = 0;
    int k = s;

    while (index1 < len1 && index2 < len2)
    {
        if (firstPart[index1] <= secondPart[index2])
        {
            arr[k] = firstPart[index1];
            index1++;
        }
        else
        {
            arr[k] = secondPart[index2];
            index2++;
        }
        k++;
    }

    while (index1 < len1)
    {
        arr[k] = firstPart[index1];
        index1++;
        k++;
    }

    while (index2 < len2)
    {
        arr[k] = secondPart[index2];
        index2++;
        k++;
    }

    delete[] firstPart;
    delete[] secondPart;
}

void merge_sort(int *arr, int s, int e)
{
    if (s >= e)
    {
        return;
    }

    int mid = s + (e - s) / 2;
    // left part
    merge_sort(arr, s, mid);
    // printArray(arr, e + 1);
    //  right part
    merge_sort(arr, mid + 1, e);
    // printArray(arr, e + 1);
    //  merging
     merge(arr, s, e);
}




int main(){
    int n;
    cout<<"Enter size of array : ";
    cin>>n;
    cout<<"Enter elements : "<< endl;
    int * arr = new int[n];
    for(int i = 0; i < n;i++){
        cin>>arr[i];
    }
    printArray(arr,n);
    //b_sort(arr,n);
    //i_sort(arr,n);
    //heapSort(arr,n);
    auto start = high_resolution_clock::now();
    merge_sort(arr,0,n-1);
    auto stop = high_resolution_clock::now();
    printArray(arr,n);
    std::chrono::duration<double, std::milli> duration = stop - start;
    
    // Output the duration in microseconds
    std::cout << "Time taken: " << duration.count()<< " milliseconds\n"<<"m_sort "<<n<<endl;

}
