#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <vector>
#include <tuple>
#include <set>

using namespace std;

int trailheadScore(const vector<vector<int>> &puzzle, int row, int col, int oldHeight, set<int> &idSet)
{
    if (row < 0 || row >= puzzle.size() || col < 0 || col >= puzzle[row].size()) { 
        return -1;
    } 

    int height = puzzle[row][col];

    // Check if new height puzzle[row][col] is exactly 1 greater
    if ( height != oldHeight + 1) { 
        return -1;
    } 

    if ( height == 9) { 
        int id = row * puzzle[row].size() + col;
        idSet.insert(id);
        return id;
    } 

    trailheadScore(puzzle, row - 1, col, height, idSet);     // UP
    trailheadScore(puzzle, row + 1, col, height, idSet);     // DOWN
    trailheadScore(puzzle, row, col - 1, height, idSet);     // LEFT
    trailheadScore(puzzle, row, col + 1, height, idSet);     // RIGHT

    return -1;
}

int trailheadRating(const vector<vector<int>> &puzzle, int row, int col, int oldHeight, vector<int> &idRating)
{
    if (row < 0 || row >= puzzle.size() || col < 0 || col >= puzzle[row].size()) { 
        return 0;
    } 

    int height = puzzle[row][col];

    // Check if new height puzzle[row][col] is exactly 1 greater
    if ( height != oldHeight + 1) { 
        return 0;
    } 

    if ( height == 9) { 
        return 1;
    }

    int rating = 0;
    int id = row * puzzle[row].size() + col;

    if ( idRating[id] != -1) { 
        return idRating[id];
    }

    rating += trailheadRating(puzzle, row - 1, col, height, idRating);     // UP
    rating += trailheadRating(puzzle, row + 1, col, height, idRating);     // DOWN
    rating += trailheadRating(puzzle, row, col - 1, height, idRating);     // LEFT
    rating += trailheadRating(puzzle, row, col + 1, height, idRating);     // RIGHT

    idRating[id] = rating;
    return rating;
}

int main()
{
    ifstream f("inputs/input.txt");
    if (!f.is_open())
    {
        cerr << "Error opening the file!";
        return 1;
    }

    int rowIdx = 0;
    string line;
    vector<vector<int>> puzzle;
    vector<tuple<int,int>> zerosIdx;        // tuple(i,j)
    while (getline(f, line))
    {
        std::vector<int> row;
        for (int i = 0; i < line.length(); i++)
        {
            row.push_back(line[i] - '0');
            if(line[i] == '0'){
                zerosIdx.push_back({rowIdx,i});
            }
        }
        puzzle.push_back(row);
        rowIdx++;
    }
    f.close();

    int sumA = 0;
    int sumB = 0;
    for(auto p : zerosIdx){
        auto [row, col] = p;
        set<int> ids;
        vector<int> ratings(puzzle.size()*puzzle[0].size(), -1);
        trailheadScore(puzzle, row, col, -1, ids);
        sumA += ids.size();
        sumB += trailheadRating(puzzle, row, col, -1, ratings);
    }
    cout << "PART A: " << sumA << endl;
    cout << "PART B: " << sumB << endl;

    return 0;
}