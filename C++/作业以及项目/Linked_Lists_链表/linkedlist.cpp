#include <iostream>
using namespace std;
#include "linkedlist.h"

int Node::getData() {
	return data;
}
void Node::setData(int newData) {
	data = newData;
}
Node* Node::getNext() {
	return next;
}
void Node::setNext(Node *newNext) {
	next = newNext;
}

LinkedList::~LinkedList() {
	Node* currNode, *preNode;
	currNode = head;
	preNode = nullptr;
	while (currNode) {
		preNode = currNode;
		currNode = currNode->getNext();
		delete preNode;
	}
}

bool LinkedList::append(int number) {
	Node* currNode, *preNode, *newNode;
	currNode = head;
	preNode = nullptr;
	newNode = new Node;
	newNode->setData(number);
	if (!currNode) {
		newNode->setNext(currNode);
		head = newNode;
		return true;
	}
	while (currNode) {
		preNode = currNode;
		currNode = currNode->getNext();
	}
	newNode->setNext(preNode->getNext());
	preNode->setNext(newNode);
	return true;
}

bool LinkedList::insert(int pos, int num) {
		if (pos < 1) { return false; }
		Node* currNode = head;
		int index = 1;
		while (currNode && ++index < pos) {
			currNode = currNode->getNext();
		}
		if (!currNode && index != 1) { return false; }
		Node *newNode = new Node;
		newNode->setData(num);
		if (pos == 1) {
			newNode->setNext(head);
			head = newNode;
		}
		else {
			newNode->setNext(currNode->getNext());
			currNode->setNext(newNode);
		}
		return true;
	}

int LinkedList::getSize() {
		Node* currNode = head;
		int index = 0;
		while (currNode) {
			index++;
			currNode = currNode->getNext();
		}
		cout << "The size is " << index << endl;
		return index;
	}

int LinkedList::search(int num) {
		Node* currNode = head;
		int index = 1;
		while (currNode && currNode->getData() != num) {
			index++;
			currNode = currNode->getNext();
		}
		if (currNode) {
			cout << "The position is " << index << endl;
			return currNode->getData();
		}
		return false;
	}

bool LinkedList::remove(int pos) {
		if (pos < 1) {
			return false;
		}
		Node* currNode, *preNode;
		preNode = nullptr;
		currNode = head;
		int index = 0;
		while (currNode && ++index<pos) {
			preNode = currNode;
			currNode = currNode->getNext();
		}
		if (!currNode) {
			return false;
		}
		if (!preNode) {
			head = currNode->getNext();
			delete currNode;
			cout << "Remove success." << endl;
			return true;
		}
		else {
			preNode->setNext(currNode->getNext());
			delete currNode;
			cout << "Remove success." << endl;
			return true;
		}
	}

void LinkedList::display() {
		Node* currNode = head;
		int index;
		index = 0;
		while (currNode) {
			index++;
			cout << "The " << index << "th number is " << currNode->getData() << endl;
			currNode = currNode->getNext();
		}
	}

Node* LinkedList::gethead() {
	return head;
}