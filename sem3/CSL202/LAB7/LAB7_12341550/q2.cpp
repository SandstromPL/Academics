#include <iostream>
#include <algorithm>

using namespace std;

struct Node
{
    int key;
    Node *left;
    Node *right;

    Node(int val)
    {
        key = val;
        left = right = nullptr;
    }
};

int computeHeight(Node *node)
{
    if (node == nullptr)
        return 0;

    int leftHeight = computeHeight(node->left);
    int rightHeight = computeHeight(node->right);

    return 1 + max(leftHeight, rightHeight);
}

void printHeights(Node *node)
{
    if (node == nullptr)
        return;

    cout << "Node " << node->key << " has height: " << computeHeight(node) << endl;

    printHeights(node->left);
    printHeights(node->right);
}

Node *insert(Node *node, int key)
{
    if (node == nullptr)
        return new Node(key);

    if (key < node->key)
        node->left = insert(node->left, key);
    else if (key > node->key)
        node->right = insert(node->right, key);

    return node;
}

int main()
{
    Node *root = nullptr;

    root = insert(root, 51);
    root = insert(root, 10);
    root = insert(root, 21);
    root = insert(root, 13);
    root = insert(root, 15);
    root = insert(root, 17);
    root = insert(root, 31);

    printHeights(root);

    return 0;
}
