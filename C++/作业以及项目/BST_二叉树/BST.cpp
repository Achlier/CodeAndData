/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   BST.cpp
 * Author: ericzhao
 *
 */

#include <cstdlib>
#include <queue>
#include <iostream>
#include <math.h>
#include "TreeNode.h"
#include "Tree.h"


using namespace std;


/*Insert node into BST, keeping the BST property. Use the method in Slide 24.*/
void InsertBSTNode(TreeNode* &root, int val){
    // Input your code here.
	if (root == NULL) {
		root = new TreeNode(val);
		root->left = root->right = NULL;
	}
	else if (val < root->data)
		InsertBSTNode(root->left,val);
	else if (val > root->data)
		InsertBSTNode(root->right,val);
}

// Insert each node into BST one by one.
void ConstructBST(TreeNode* &root, int* array, int arrayLength){
    //Since the first element is root, insertion starts from the 2nd element.
    for(int i=1; i<arrayLength; i++){ 
        InsertBSTNode(root, array[i]);
    }
}

Tree::Tree(int* array, int arrayLength){
    root = new TreeNode(array[0]); //Treat first element as root.
    
    ConstructBST(root, array, arrayLength);
}



/**Pre-order traverse the constructed tree. The pointer to tree root is "root".*/
void Tree::PreTraversal(TreeNode* root){
    // Input your code here.
	if (root != NULL) {
		cout << root->data << " ";
		PreTraversal(root->left);
		PreTraversal(root->right);
	}
}

void Tree::InTraversal(TreeNode* root){
    // Input your code here.
	if (root != NULL) {
		InTraversal(root->left);
		cout << root->data << " ";
		InTraversal(root->right);
	}
}

void Tree::PostTraversal(TreeNode* root){
    // Input your code here.
	if (root != NULL) {
		PostTraversal(root->left);
		PostTraversal(root->right);
		cout << root->data << " ";
	}
}

/*Output the hight of the tree. 
 The exact definition of tree hight is learned in Slide 5.
 Assume single node tree has hight 1.*/
int max(int A, int B) {
	if (A > B) { return A;}
	else { return B;}
}

int Tree::TreeHight(TreeNode* root){
    // Input your code here.
	if (root == NULL) { return 0;}
	return max(TreeHight(root->left), TreeHight(root->right)) + 1;
}

/*Do a binary search. If input value "val" is found in BST, return true, else return false.*/
bool Tree::Search(TreeNode* root, int val){
    // Input your code here.
	if (root == NULL) { return NULL; }
	else if (root->data > val) { return Search(root->left,val);}
	else if (root->data < val) { return Search(root->right,val);}
	else { return true;}
}

/* Determine if a BST is height-balanced. If balance return true, else return false.
 * A height-balanced binary tree is defined as a binary tree in which the depth
 *  of the two subtrees of every node never differ by more than 1.*/
bool Tree::IsBalanced(TreeNode* root){
    // Input your code here.
	if (root == NULL) { return true; }
	else if (!IsBalanced(root->left) || !IsBalanced(root->right)) return false;
	if (abs(TreeHight(root->left) - TreeHight(root->right)) >1) return false;
	else return true;
}

/*
 * 
 */
int main(int argc, char** argv) {
    /*Construct the tree using integers in the array. 
     * Here I just randomly pick an array, however you need to test your program by attempting different input arrays.*/
    int array[] = {5,3,6,2,4,7};   
   
    int ArrayLength = sizeof(array)/sizeof(int);
    cout << "array length is: " << ArrayLength << endl;
    
    Tree* t = new Tree(array, ArrayLength); 
    
    cout << "Construct of the Binary Search Tree is complete." << endl;
    cout << "Pre-order Traversal: ";
    t->PreTraversal(t->GetRoot());
    cout << endl << "In-order Traversal: ";
    t->InTraversal(t->GetRoot());
    cout << endl << "Post-order Traversal: ";
    t->PostTraversal(t->GetRoot());
    cout << endl << "Tree hight is: " << t->TreeHight(t->GetRoot()) << endl;
    //Given a value, use binary search to find if it exists 
    int val = 9;
    if (t->Search(t->GetRoot(), val)) cout << val << "is found" << endl;
    else cout << val << "is not found in tree" << endl;
    // Check if the BST is height-balanced or not.
    if(t->IsBalanced(t->GetRoot())) cout << "BST is balanced" << endl;
    else cout << "BST is not balanced" << endl;
	system("PAUSE");
    return 0;
}

