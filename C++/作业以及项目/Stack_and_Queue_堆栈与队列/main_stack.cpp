#include <iostream>
using namespace std;
#include "Stack_Queue.h"

Stack::Stack(int size) {
	maxTop = size - 1;
	top = -1;
	values = new double[size];
}


double Stack::Top() {
	if (IsEmpty()) {
		cout << "This stack is empty."<<endl;
		return -1;
	}
	else {
		return values[top];
	}
}

void Stack::Push(const double x) {
	if (IsFull()) {
		cout << "This stack is full." << endl;
	}
	else {
		values[++top] = x;
	}
}

double Stack::Pop() {
	if (IsEmpty()) {
		cout << "This stack is empty." << endl;
		return -1;
	}
	else {
		double num = values[top--];
		return num;
	}
}

void Stack::DisplayStack() {
	if (IsEmpty()) {
		cout << "This stack is empty." << endl;
	}
	for (int i = top; i >= 0; i--) {
		cout << "The " << maxTop - i << "th number is " << values[i] << endl;
	}
}
/*
int main(void) {
Stack stack(5);
stack.Push(5.0);
stack.Push(6.5);
stack.Push(-3.0);
stack.Push(-8.0);
stack.DisplayStack();
cout << "Top: " << stack.Top() << endl;
stack.Pop();
cout << "Top: " << stack.Top() << endl; while (!stack.IsEmpty()) stack.Pop(); stack.DisplayStack();
system("PAUSE");
return 0;
}*/