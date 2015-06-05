#include <iostream>
#include <string>
using namespace std;
void print_seq(int n, string& s, int pos, int sign) {
    char first = sign==1? '0': '9';
    if (n == 1) {
        for (int i = 0; i < 10; i++) {
            s[pos] = first + sign * i;
            cout << s << "\n";
        }
        return;
    }
    for (int i = 0; i < 10; i++) {
        s[pos] = first + sign * i;
        print_seq(n-1, s, pos+1, i%2? -1: 1);
    }
}

int main() {
    int n;
	while (cin >> n) {
		cout << string(n, '9') << "\n";
		string s(n, '0');
		print_seq(n, s, 0, 1);
	}
    return 0;
}