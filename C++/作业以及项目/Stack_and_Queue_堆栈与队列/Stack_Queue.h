/*Problem 1: 
Below are the Stack and Queue ADT shown in lecture slides. Implement both Stack and Queue ADT methods and put it in a .cpp file*/

class Stack {
	public: 
		Stack(int size = 10); // constructor 
		~Stack() { delete [] values; } // destructor
		bool IsEmpty() { return top == -1; }
		bool IsFull() { return top == maxTop; }
		double Top(); // examine, without popping 
		void Push(const double x);
		double Pop();
		void DisplayStack();
	private:
		int maxTop;; // max stack size = size - 1 
		int top; // current top of stack
		double* values; // element array
};

class Queue {
	public: 
		Queue(int size = 10); // constructor 
		~Queue() { delete [] values; }  // destructor
		bool IsEmpty(void);
		bool IsFull(void);
		bool Enqueue(double x); 
		bool Dequeue(double & x); 
		void DisplayQueue(void);
	private:
		int front; 	// front index
		int rear;	// rear index
		int counter;	// number of elements	
		int maxSize; // size of array queue
		double* values; // element array 
};