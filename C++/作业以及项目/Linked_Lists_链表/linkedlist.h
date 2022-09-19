/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   LinkedList.h
 * Author: ericzhao
 */

#ifndef LINKEDLIST_H
#define LINKEDLIST_H

#include <iostream>
using namespace std;

class Node{
private:
    int data;
    Node *next;
    
public:
    Node(): data(0), next(nullptr) {}
    int getData();
    void setData(int newData);
    Node *getNext();
    void setNext(Node *newNext);
};

class LinkedList{
private:
    Node *head;
    friend class ListStack;
    
public:
    LinkedList(): head(nullptr) {}
    ~LinkedList();
    /*Append element to the end of the list*/
    bool append(int number);
	/*Insert an element "num" at specific position "pos".
	If "pos==1", insert "num" as the first element.
	"pos" should larger or equal 1. It is invalid to insert into an empty list. (Raise error for these cases.)*/
    bool insert(int pos, int num);
    /*The number of elements in the list*/
    int getSize();
    /*Search element "num" from list. If exits, return true; else return false;*/
    int search(int num);
    /*Remove an element at position "index". If fail to remove, return false;*/
    bool remove(int pos);
    /*Print out all elements in the linked list*/
    void display();  
	Node *gethead();
};


#endif /* LINKEDLIST_H */

