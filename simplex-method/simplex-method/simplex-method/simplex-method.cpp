// simplex-method.cpp: определяет точку входа для приложения.
//

#include "simplex-method.h"

using namespace std;

int main() {
	canon_task task(string("../../../../resource/task.txt"));

	if (errorSingleton::GetInstance().isError())
		std::cout << errorSingleton::GetInstance().GetMessage() << "\n";
	else
		task.print();

	return 0;
}
