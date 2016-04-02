
int func1(int i, int j) {
	int _i, _j;
	_i = i;
	_j = j;
}

class MyClassB
{
	int _i_B;
	char _j_B;
	MyClassA _A;
	void memfunc_B() {
		_i_B = 0;
		_j_B = 1;
		_A.memfunc_A(_i_B, _j_B);
	}
};

class MyClassA
{
	int _i_A;
	char _j_A;
	void memfunc_A(int i, int j) {
		_i_A = i;
		_j_A = j;
	}
};

int main() {
	int _i=1;
	int _j=2;
	func1(_i, _j);
	func1(3, 4);
	MyClassB _B1;
	MyClassB _B2;
	_B1.memfunc_B();
	_B2.memfunc_B();
}

