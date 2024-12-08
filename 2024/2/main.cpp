#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <string>

using namespace std;

bool checkSafe(vector<int> data){
    int diff;
    bool desc;
    bool safe = true;
    desc = data[0] > data[1];
    for (int i = 1; i < data.size(); ++i) {
        diff = data[i] - data[i - 1];
        if (abs(diff) > 3 || diff == 0 || desc != data[i - 1] > data[i]){
            safe = false;
            break;
        }
        desc = data[i - 1] > data[i];
    }
    return safe;
}

int main() {
    
    ifstream f("inputs/input.txt");
    if (!f.is_open()) {
        cerr << "Error opening the file!";
        return 1;
    }

    string report;
    int countSafeA = 0;
    int countSafeB = 0;

    while (getline(f, report)){
        vector<int> data;
        int number; 
        stringstream ss(report);

        while (ss >> number) {
            data.push_back(number);
        }

        if(checkSafe(data)){
            countSafeA += 1;
        }
        else{
            for (int i = 0; i < data.size(); ++i) {
                vector<int> subset = data;
                subset.erase(subset.begin() + i);
                if (checkSafe(subset)){
                    countSafeB += 1;
                    break;
                }
            }
        }

    }
    cout << "PART A: "<< countSafeA << endl;
    cout << "PART B: "<< countSafeA + countSafeB;

    f.close();
    return 0;
}