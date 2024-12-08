#include <iostream>
#include <fstream>
#include <string>
#include <regex>

using namespace std;

int mul(const string &s)
{
    regex pattern("mul\\((\\d{1,3}),(\\d{1,3})\\)");
    smatch match;
    if (regex_search(s, match, pattern))
    {
        int num1 = stoi(match[1]);
        int num2 = stoi(match[2]);
        return num1 * num2;
    }
    return 0;
}

int sumInput(const string &line)
{
    int sumInput = 0;
    regex mulPattern("mul\\(\\d{1,3},\\d{1,3}\\)");
    sregex_iterator begin(line.begin(), line.end(), mulPattern);
    sregex_iterator end;

    for (sregex_iterator it = begin; it != end; ++it)
    {
        sumInput += mul(it->str());
    }
    return sumInput; 
}

int main()
{

    ifstream f("inputs/input.txt");
    if (!f.is_open())
    {
        cerr << "Error opening the file!";
        return 1;
    }

    string line;
    string input = "";
    regex doPattern("don't\\(\\)(.*?)(do\\(\\)|$)");
    int sumA = 0;
    int sumB = 0;

    while (getline(f, line))
    {
        input += line;
    }

    cout << "PART A: " << sumInput(input) << endl;

    string inputB = regex_replace(input, doPattern, "");
    cout << "PART B: " << sumInput(inputB) << endl;

    f.close();
    return 0;
}