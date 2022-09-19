/*Problem 2: Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

push(x) -- Push element x onto stack.
pop() -- Removes the element on top of the stack.
top() -- Get the top element.
getMin() -- Retrieve the minimum element in the stack.
Example:
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> Returns -3.
minStack.pop();
minStack.top();      --> Returns 0.
minStack.getMin();   --> Returns -2.*/
#include <iostream>
using namespace std;

class Node {
private:
	int data;
	Node *next;

public:
	Node() : data(0), next(nullptr) {}
	int getData() {
		return data;
	}
	void setData(int newData) {
		data = newData;
	}
	Node *getNext() {
		return next;
	}
	void setNext(Node *newNext) {
		next = newNext;
	}
};

class MinStack {
	private:
		Node *head;
	public:
		MinStack() : head(nullptr) {}
		void push(int x) {
			Node*newNode = new Node;
			newNode->setData(x);
			newNode->setNext(head);
			head = newNode;
		}
    
		void pop() {
			if (!head) {
				cout << "empty" << endl;
			}
			else {
				Node*temNode = head;
				head = head->getNext();
				delete temNode;
			}
		}
    
		int top() {
			if (!head) {
				cout << "empty" << endl;
				return -1;
			}
			return head->getData();
		}
    
		int getMin() {
			if (!head) {
				cout << "empty" << endl;
				return -1;
			}
			int min = NULL;
			Node* currNode = head;
			while (currNode) {
				if (currNode->getData()<min){
					min = currNode->getData();
				}
				currNode = currNode->getNext();
			}
			cout << "The min is " << min << endl;
			return min;
		}
};
/**/
int main() {
	MinStack minStack =MinStack();
	minStack.push(-2);
	minStack.push(0);
	minStack.push(-3);
	minStack.getMin();
	minStack.pop();
	minStack.top();
	minStack.getMin();
	system("PAUSE");
	return 0;
}
/**
 * Your MinStack object will be instantiated and called as such:
 * MinStack obj = new MinStack();
 * obj.push(x);
 * obj.pop();
 * int param_3 = obj.top();
 * int param_4 = obj.getMin();
 */