#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;


int countWords(const vector<vector<char>> &puzzle, const int &i, const int &j, const vector<char> &pattern){
    // {i,j}
    vector<vector<int>> dir = {{0,1},       // right
                                {0,-1},     // left
                                {-1,0},     // up
                                {1,0},      // down
                                {-1,1},     // right up
                                {1,1},     // right down
                                {-1,-1},    // left up
                                {1,-1}};     // left down
    int count = 0;

    for (int possible = 0; possible < dir.size(); possible++) {
        bool isMatch = true;
        for(int pos = 1; pos < pattern.size(); pos++){
            int nextI = dir[possible][0] * pos + i;
            int nextJ = dir[possible][1] * pos + j;
            if (nextI < 0 || nextI >= puzzle.size() || nextJ < 0 || nextJ >= puzzle[nextI].size()) {
                isMatch = false;
                break;
            }
            //cout << "POSSIBLE: " << possible << endl;
            //cout << "i= " << nextI << " j= " << nextJ << "   char: " << puzzle.at(nextI).at(nextJ) << endl;
            if(puzzle.at(nextI).at(nextJ) != pattern[pos]){
                isMatch = false;
                break;
            }
        }
        if(isMatch){
            count += 1;
        }
    }
    return count;
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
    vector<vector<char>> puzzle;
    vector<char> pattern = {'X', 'M', 'A', 'S'};


    while (getline(f, line))
    {
        puzzle.push_back(vector<char>(line.begin(), line.end()));
    }
    f.close();

    int sumA = 0;
    // i = row
    // j = col
    for (int i = 0; i < puzzle.size(); i++) {
        for (int j = 0; j < puzzle[i].size(); j++) {
            if(puzzle[i][j] == pattern[0]){
                sumA += countWords(puzzle, i, j, pattern);
            }
        }
    }
    cout << sumA;
    return 0;
}