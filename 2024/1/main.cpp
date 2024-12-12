#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
using namespace std;

// Comparator function
bool comp(int a, int b) {
    return a < b;
}

int main() {
    vector<int> vec1, vec2, vecDif;
    int value1, value2;

    // Read from the text file
    ifstream MyReadFile("inputs/input.txt");

    while (MyReadFile >> value1 >> value2) {
        vec1.push_back(value1); // first Value -> Vec1
        vec2.push_back(value2); // second Value -> Vec2
    }
    MyReadFile.close();

    sort(vec1.begin(),vec1.end(),comp);
    sort(vec2.begin(),vec2.end(),comp);

    transform(vec1.begin(), vec1.end(), vec2.begin(), std::back_inserter(vecDif), [&](double l, double r)
    {
        return abs(l - r);
    });

    int result1;
    for (auto& n : vecDif){
        result1 += n;
    }
    cout << "PART A " << result1;
    cout << endl;

    // Part 2
    int frequency, result2;
    for (auto& n : vec1){
        frequency = count(vec2.begin(), vec2.end(), n);
        result2 += n * frequency;
    }
    cout << "PART B " << result2;
    
    return 0;
}
