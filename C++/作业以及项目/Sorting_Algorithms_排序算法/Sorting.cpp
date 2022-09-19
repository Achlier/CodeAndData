/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   main.cpp
 * Author: ericzhao
 *
 * Created on March 18, 2017, 5:33 PM
 */

#include <cstdlib>
#include "Sorting.h"
#include "stdio.h"
#include "array"
#include <iostream>
#include <ctime>
#include <cmath>
using namespace std;

/*Create an array of random numbers with length k*/
void Sorting::CreateArray(int k){
    NumList = new int[k];
    for (int i=0; i<k; i++){
        NumList[i] = rand()%(k+10);
    }
    num = k;
}

/*Copy the created array*/
int* Sorting::CopyArray(){
    int* list = new int[num];
    for(int i=0; i<num; i++){
        list[i] = *(NumList+i);
    }
    return list;
}

void Sorting::Print(int* NumList){
    for(int i=0; i<num; i++){
        cout << NumList[i] << ",";
    }
    cout << endl;
}

/**==========================For Bubble Sort===================================*/
void Sorting::BubbleSort(int* NumList) {
	for (int i = 0; i < num - 1; i++) {
		for (int j = 0; j < num - i - 1; j++) {
			if (NumList[j] > NumList[j + 1]) {
				int temp = NumList[j + 1];
				NumList[j + 1] = NumList[j];
				NumList[j] = temp;
			}
		}
	}
}

/**==========================For Insertion Sort===================================*/
void Sorting::InsertSort(int* NumList) {
	for (int i = 1; i < num ; i++) {
		int temp = NumList[i];
		for (int j = i; ; j--)
			if (j > 0 && temp < NumList[j - 1])
				NumList[j] = NumList[j - 1];
			else {
				NumList[j] = temp;
				break;
			}
	}
}

/**==========================For Merge Sort===================================*/

/*Merge two sorted array. Used in MergeSort*/
void Merge(int* NumList, int start, int mid, int end) {
	int pa = start, pb = mid, n = 0;
	int * T = new int[end - start + 1];
	while (pa <= mid - 1 && pb <= end) {
		if (NumList[pa] < NumList[pb]) {
			T[n] = NumList[pa];
			pa++;
			n++;
		}
		else {
			T[n] = NumList[pb];
			pb++;
			n++;
		}
	}
	while (pa <= mid - 1) {
		T[n] = NumList[pa];
		pa++;
		n++;
	}
	while (pb <= end) {
		T[n] = NumList[pb];
		pb++;
		n++;
	}
	for (n = 0; start <= end; start++, n++) {
		NumList[start] = T[n];
	}
	delete T;
}

void Sorting::MergeSort(int* NumList, int start, int end) {
	if (start < end) {
		int center = (start + end) / 2;
		MergeSort(NumList, start, center);
		MergeSort(NumList, center + 1, end);
		Merge(NumList, start, center + 1, end);
	}

}

/**==========================For Quick Sort===================================*/
/*Swap the i'th and j'th element in the array*/
void Swap(int* NumList, int i, int j) {
	int temp = NumList[i];
	NumList[i] = NumList[j];
	NumList[j] = temp;
}

int MedianOfThree(int* NumList, int begin, int tail) {
	int center = (begin + tail) / 2;
	if (NumList[center] < NumList[begin])
		Swap(NumList, begin, center);
	if (NumList[tail] < NumList[begin])
		Swap(NumList, begin, tail);
	if (NumList[tail] < NumList[center])
		Swap(NumList, center, tail);
	Swap(NumList, center, tail - 1);
	return NumList[tail - 1];
}

int Partition(int* NumList, int begin, int tail) {
	int center = MedianOfThree(NumList, begin, tail);
	int ll = begin, rr = tail - 1;
	while (true) {
		while (NumList[++ll]<center) {}
		while (center<NumList[--rr]) {}
		if (ll < rr)
			Swap(NumList, ll, rr);
		else
			break;
	}
	Swap(NumList, ll, tail - 1);
	return ll;
}

void Sorting::QuickSort(int* NumList, int begin, int tail) {
	if (begin < tail) {
		int center = Partition(NumList, begin, tail);
		QuickSort(NumList, begin, center - 1);
		QuickSort(NumList, center + 1, tail);
	}

}

/**==========================For Heap Sort===================================*/

/**Maintain min-heap order*/
void percolateUp(int* heap, int currentSize){
	int temp = heap[currentSize];
	for (; currentSize > 1 && temp >heap[currentSize / 2]; currentSize /= 2) {
		heap[currentSize] = heap[currentSize / 2];
	}
	heap[currentSize] = temp;
}

/**Append an element to the end of heap, and adjust heap to maintain the min-heap order.*/
void InsertHeap(int* heap, int& currentSize, const int num){
	heap[++currentSize] = num;
	percolateUp(heap, currentSize);
}

/**Construct a min heap (Parent larger than its children)*/
int* BuildMaxHeap(int* NumList, int num){
	int currentSize = 0;
	int* heap = new int[num+1];
	heap[0] = 0;
	for (int i = 0; i < num; i++) {
		InsertHeap(heap, currentSize, NumList[i]);
	}
	return heap;
}

/**Adjust heap to maintain the heap order*/
void percolateDown(int* heap, int currentSize){
	int child = 1, temp = heap[1];
	for (int hole = 1; hole * 2 <= currentSize; hole = child) {
		child = hole * 2;
		if (child != currentSize&&heap[child + 1] > heap[child]) {child++; }
		if (heap[child] > temp) { heap[hole] = heap[child];heap[child] = temp;}
		else { break; }
	}
	
}

void DeleteMax(int* heap, int& currentSize){
	if (currentSize == 0) { return; }
	int temp = heap[1];
	heap[1] = heap[currentSize];
	heap[currentSize--] = temp;
	percolateDown(heap,currentSize);
}

void* Sorting::HeapSort(int* NumList){
	int* heap = BuildMaxHeap(NumList, num);
	int currentSize = num;
	for (; currentSize!=1;) {
		DeleteMax(heap, currentSize);
	}
	for (int i = 0; i < num; i++) {
		NumList[i]= heap[i+1];
	}
	return heap;
}


int main(int argc, char** argv) {
	for (int time = 3; time <= 17; time++) {
		cout << " The times is " << time << endl;
		Sorting s;
		int t = time; //You may try different numbers here, e.g. from 3 to 17.
		int num = pow(2, t);
		s.CreateArray(num);  //Created an Array "A" with "num" elements.
		clock_t start;
		double duration; //Time duration of running each sorting algorithm.

		int* BubbleSortList = s.CopyArray();  //Copy array "A" for BubbleSort.
		start = std::clock();    //Start timer.
		s.BubbleSort(BubbleSortList);       //Run sorting algorithm;
		duration = (std::clock() - start) / (double)CLOCKS_PER_SEC;  //Record running time.
		cout << "Bubble Sort needs time: " << duration << endl;
	


		int* InsertSortList = s.CopyArray();
		start = std::clock();
		s.InsertSort(InsertSortList);
		duration = (std::clock() - start) / (double)CLOCKS_PER_SEC;
		cout << "Insertion Sort needs time: " << duration << endl;
		

		int* MergeSortList = s.CopyArray();
		start = std::clock();
		s.MergeSort(MergeSortList, 0, num - 1);
		duration = (std::clock() - start) / (double)CLOCKS_PER_SEC;
		cout << "Merge Sort needs time: " << duration << endl;
	

		int* QuickSortList = s.CopyArray();
		start = std::clock();
		s.QuickSort(QuickSortList, 0, num - 1);
		duration = (std::clock() - start) / (double)CLOCKS_PER_SEC;
		cout << "Quick Sort needs time: " << duration << endl;


		int* HeapSortList = s.CopyArray();
		start = std::clock();
		s.HeapSort(HeapSortList);
		duration = (std::clock() - start) / (double)CLOCKS_PER_SEC;
		cout << "Heap Sort needs time: " << duration << endl;
		cout << "-----------------" << endl;
	}
	system("PAUSE");

    return 0;
}

