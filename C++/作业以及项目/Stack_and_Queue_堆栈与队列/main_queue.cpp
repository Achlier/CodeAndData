#include <iostream>
using namespace std;
#include "Stack_Queue.h"

Queue::Queue(int size) {
	maxSize = size;
	counter = 0;
	rear = -1;
	front = 0;
	values = new double[size];
}

bool Queue::IsEmpty(void) {
	return counter == 0;
}

bool Queue::IsFull(void) {
	return counter == maxSize;
}

bool Queue::Enqueue(double x) {
	if (IsFull()) {
		cout << "This queue is full." << endl;
		return false;
	}
	else {
		counter++;
		rear = (rear + 1) % maxSize;
		values[rear] = x;
		return true;
	}
}

bool Queue::Dequeue(double & x) {
	if (IsEmpty()) {
		cout << "This queue is empty." << endl;
		return false;
	}
	else {
		counter--;
		x = values[front];
		front= (front + 1) % maxSize;
		return true;
	}
}

void Queue::DisplayQueue(void) {
	if (IsEmpty()) {
		cout << "This queue is empty." << endl;
	}
	else {
		cout << "The front -->" << endl;
		for (int curr = front;;) {
			if (curr == rear) {
				cout << "             " << values[curr] << "<-- The end" << endl;
				break;
			}
			cout << "             "<<values[curr] << endl;
			curr = (curr + 1) % maxSize;
			
		}
	}
}
/*
int main(void) {
	Queue queue(5);
	cout << "Enqueue 5 items." << endl; for (int x = 0; x < 5; x++)
	queue.Enqueue(x);
	cout << "Now attempting to enqueue again..." << endl; queue.Enqueue(5);
	queue.DisplayQueue();
	double value;
	queue.Dequeue(value);
	cout << "Retrieved element = " << value << endl; queue.DisplayQueue();
	queue.Enqueue(7);
	queue.DisplayQueue();
	system("PAUSE");
	return 0;
}*/