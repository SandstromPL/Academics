#include <iostream>
using namespace std;

// Structure to represent a node in the BST
struct TreeNode {
    int value;
    TreeNode* leftChild;
    TreeNode* rightChild;

    TreeNode(int val) : value(val), leftChild(nullptr), rightChild(nullptr) {}
};

// Class to implement the BST with various operations
class BinarySearchTree {
private:
    TreeNode* root;

    // Helper function to insert a new node
    TreeNode* addNode(TreeNode* node, int value) {
        if (!node) return new TreeNode(value);
        if (value < node->value)
            node->leftChild = addNode(node->leftChild, value);
        else
            node->rightChild = addNode(node->rightChild, value);
        return node;
    }

    // Helper function to find the smallest node
    TreeNode* findMinNode(TreeNode* node) {
        while (node && node->leftChild)
            node = node->leftChild;
        return node;
    }

    // Helper function to find the largest node
    TreeNode* findMaxNode(TreeNode* node) {
        while (node && node->rightChild)
            node = node->rightChild;
        return node;
    }

    // Helper functions for different types of tree traversal
    void traverseInOrder(TreeNode* node) {
        if (node) {
            traverseInOrder(node->leftChild);
            cout << node->value << " ";
            traverseInOrder(node->rightChild);
        }
    }

    void traversePreOrder(TreeNode* node) {
        if (node) {
            cout << node->value << " ";
            traversePreOrder(node->leftChild);
            traversePreOrder(node->rightChild);
        }
    }

    void traversePostOrder(TreeNode* node) {
        if (node) {
            traversePostOrder(node->leftChild);
            traversePostOrder(node->rightChild);
            cout << node->value << " ";
        }
    }

    // Helper function to remove a node
    TreeNode* removeNode(TreeNode* node, int value) {
        if (!node) return node;
        if (value < node->value)
            node->leftChild = removeNode(node->leftChild, value);
        else if (value > node->value)
            node->rightChild = removeNode(node->rightChild, value);
        else {
            if (!node->leftChild) {
                TreeNode* temp = node->rightChild;
                delete node;
                return temp;
            } else if (!node->rightChild) {
                TreeNode* temp = node->leftChild;
                delete node;
                return temp;
            }
            TreeNode* temp = findMinNode(node->rightChild);
            node->value = temp->value;
            node->rightChild = removeNode(node->rightChild, temp->value);
        }
        return node;
    }

    // Helper function to find the successor of a node
    TreeNode* findSuccessor(TreeNode* node, int value) {
        TreeNode* current = searchNode(root, value);
        if (!current) return nullptr;

        if (current->rightChild) {
            return findMinNode(current->rightChild);
        }

        TreeNode* successor = nullptr;
        TreeNode* ancestor = root;
        while (ancestor != current) {
            if (value < ancestor->value) {
                successor = ancestor;
                ancestor = ancestor->leftChild;
            } else {
                ancestor = ancestor->rightChild;
            }
        }
        return successor;
    }

    // Helper function to search for a node
    TreeNode* searchNode(TreeNode* node, int value) {
        while (node && node->value != value) {
            if (value < node->value) node = node->leftChild;
            else node = node->rightChild;
        }
        return node;
    }

    // Helper function to calculate the height of the tree
    int calculateHeight(TreeNode* node) {
        if (!node) return 0;
        int leftHeight = calculateHeight(node->leftChild);
        int rightHeight = calculateHeight(node->rightChild);
        return max(leftHeight, rightHeight) + 1;
    }

public:
    BinarySearchTree() : root(nullptr) {}

    // Public methods to access private members
    void insert(int value) {
        root = addNode(root, value);
    }

    void remove(int value) {
        root = removeNode(root, value);
    }

    void printMin() {
        TreeNode* minNode = findMinNode(root);
        if (minNode) cout << "Minimum value: " << minNode->value << endl;
        else cout << "The tree is empty." << endl;
    }

    void printMax() {
        TreeNode* maxNode = findMaxNode(root);
        if (maxNode) cout << "Maximum value: " << maxNode->value << endl;
        else cout << "The tree is empty." << endl;
    }

    void printPreOrder() {
        cout << "Preorder Traversal: ";
        traversePreOrder(root);
        cout << endl;
    }

    void printInOrder() {
        cout << "Inorder Traversal: ";
        traverseInOrder(root);
        cout << endl;
    }

    void printPostOrder() {
        cout << "Postorder Traversal: ";
        traversePostOrder(root);
        cout << endl;
    }

    void printSuccessor(int value) {
        TreeNode* successor = findSuccessor(root, value);
        if (successor) cout << "Successor of " << value << " is " << successor->value << endl;
        else cout << "Successor not found." << endl;
    }

    void printHeight() {
        cout << "Height of the tree: " << calculateHeight(root) << endl;
    }
};

int main() {
    BinarySearchTree bst;
    bst.insert(20);
    bst.insert(10);
    bst.insert(30);
    bst.insert(5);
    bst.insert(15);
    bst.insert(25);
    bst.insert(35);

    bst.printPreOrder();
    bst.printInOrder();
    bst.printPostOrder();

    bst.printMin();
    bst.printMax();

    bst.printHeight();

    bst.printSuccessor(15);
    bst.remove(20);
    bst.printInOrder();

    return 0;
}