#include <iostream>
#include <vector> 
#include <list>
#include <queue>
using namespace std;

vector<list<int>> ini() {
	list<int>v0{ 8 };
	list<int>v1{ 2,3,7,9 };
	list<int>v2{ 1,4,8 };
	list<int>v3{ 1,4,5 };
	list<int>v4{ 2,3 };
	list<int>v5{ 3,6 };
	list<int>v6{ 5,7 };
	list<int>v7{ 1,6 };
	list<int>v8{ 0,2,9 };
	list<int>v9{ 1,8 };
	vector<list<int>>List{ v0,v1,v2,v3,v4,v5,v6,v7,v8,v9 };
	return List;
}

void Path(vector<int> pred, int Tvertex) {
	if (pred[Tvertex] != -1) {
		Path(pred, pred[Tvertex]);
	}
	cout << Tvertex << " " ;
}


void BFS(vector<list<int>>List, int Overtex , int Tvertex) {
	vector<bool> flag(10,false);
	vector<int> pred(10, -1);
	queue<int> Q;
	flag[Overtex] = true;
	Q.push(Overtex);
	int currvertex;
	while (!Q.empty()) {
		currvertex = Q.front();
		Q.pop();
		for (list<int>::const_iterator iter = List[currvertex].begin(); iter != List[currvertex].end(); iter++)
		{
			if (!flag[*iter]) {
				flag[*iter] = true;
				pred[*iter] = currvertex;
				Q.push(*iter);
			}
		}
	}
	Path(pred,Tvertex);
	cout << endl;
}

void RDFS(vector<list<int>>List, int Overtex, int Tvertex, vector<bool>&flag, vector<int>&pred) {
	for (list<int>::const_iterator iter = List[Overtex].begin(); iter != List[Overtex].end(); iter++)
	{
		if (!flag[*iter]) {
			flag[*iter] = true;
			pred[*iter] = Overtex;
			RDFS(List, *iter, Tvertex, flag, pred);
		}
	}
}

void DFS(vector<list<int>>List, int Overtex, int Tvertex) {
	vector<bool> flag(10, false);
	vector<int> pred(10, -1);
	flag[Overtex] = true;
	RDFS(List, Overtex, Tvertex, flag, pred);
	Path(pred, Tvertex);
	cout << endl;
}

int main() {
	vector<list<int>>List = ini();
	cout << "Enter the target vertex:";
	int Tvertex;
	cin >> Tvertex;
	cout << "BFS: ";
	BFS(List, 2 ,Tvertex);
	cout << "DFS: ";
	DFS(List, 2, Tvertex);
	system("PAUSE");
}