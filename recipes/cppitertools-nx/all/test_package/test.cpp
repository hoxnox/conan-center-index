#include <cppitertools/shuffled.hpp>
#include <set>
#include <iostream>

int main(int argc, char* argv[])
{
	std::set<int> nums{4, 0, 2, 1, 3};
	std::string delim;
	for (auto&& i : iter::shuffled(nums))
	{
		std::cout << delim << i;
		delim = " ";
	}
}

