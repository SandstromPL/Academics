#include<iostream>
using namespace std;

class BSTree{
    public :
        int data;
        BSTree * left;
        BSTree * right;

        BSTree(int data){
            this -> data = data;
            this -> left = nullptr;
            this -> right = nullptr;
        }
        // inserting element
        BSTree * insertNode(BSTree * root,int data){
            if(root == nullptr){
                BSTree * temp = new BSTree(data);
                return temp;
            }
            if(data < root -> data){
                root -> left = insertNode(root -> left,data);
            }else{
                root -> right = insertNode(root -> right,data);
            }
            return root;
        }
        // finding min element
        BSTree * minElement(BSTree * root){
            BSTree * temp = root;
            while(temp && temp -> left != nullptr){
                temp = temp -> left;
            }
            return temp;
        }
        // finding max element
        BSTree * maxElement(BSTree * root){
            BSTree * temp = root;
            while(temp && temp -> right != nullptr){
                temp = temp -> right;
            }
            return temp;
        }
        // preorder traversal
        void preorderTraversal(BSTree * root){
            if(root != nullptr){
                cout << root -> data << " ";
                preorderTraversal(root -> left);
                preorderTraversal(root -> right);
            }
        }
        // postorder traversal
        void postorderTraversal(BSTree * root){
            if(root != nullptr){
                postorderTraversal(root -> left);
                postorderTraversal(root -> right);
                cout<< root -> data << " ";
            }
        }
        // inorder traversal
        void inorderTraversal(BSTree * root){
            if(root != nullptr){
                inorderTraversal(root -> left);
                cout<< root -> data << " ";
                inorderTraversal(root -> right);
            }
        }
        BSTree * DeleteNode(BSTree * root,int data){
            // case 1 : node with no child
            // case 2 : node with 1 child
            // case 3 : node with 2 children
            if(root == nullptr){
                return root;
            }
            if(data < root -> data){
                root -> left = DeleteNode(root -> left,data);
            }else if(data > root -> data){
                root -> right = DeleteNode(root -> right,data);
            }else{
                if(root -> left == nullptr){
                    BSTree * temp = root -> right;
                    delete root;
                    return temp;
                }else if(root -> right == nullptr){
                    BSTree * temp = root -> left;
                    delete root;
                    return temp;
                }

                BSTree * temp = minElement(root -> right);
                root -> data = temp -> data;
                root -> right = DeleteNode(root -> right,temp -> data);
            }
            return root;
        }

        BSTree * getSucc(BSTree * root, int target) {
    
            if (root == nullptr)
                return nullptr;
            
            if ( root->data == target && root->right != nullptr)
                return minElement(root->right);

            BSTree* succ = nullptr;
            BSTree* curr = root; 
            while (curr != nullptr) {
            
            if (target < curr->data) {
                succ = curr;
                curr = curr->left;
            }
            
            else if (target > curr->data) 
                curr = curr->right;
            
            else 
                break;
            }

            return succ;
        }

        int height(BSTree * root){
            if (root == nullptr)
            return 0;

        int lDepth = height(root->left);
        int rDepth = height(root->right);

        return max(lDepth, rDepth) + 1;
        }
};



int main()
{

    return 0;
}