#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <vector>
#include <tuple>

using namespace std;

void moveBlocksA(vector<int> &blocks)
{
    int lastBlockIdx;
    vector<int>::reverse_iterator it;

    for (int i = 0; i < blocks.size(); i++)
    {

        // for(int& j : blocks) {
        //     cout << j << " ";
        // }
        // cout << endl;

        if (blocks[i] == -1)
        {
            it = find_if_not(blocks.rbegin(), blocks.rend(), [free = -1](int element)
                             { return free == element; });
            vector<int>::iterator normalIt = it.base();
            lastBlockIdx = std::distance(blocks.begin(), normalIt) - 1;
            if (i >= lastBlockIdx)
            {
                break;
            }
            blocks[i] = blocks[lastBlockIdx];
            blocks[lastBlockIdx] = -1;
        }
    }
}

void moveBlocksB(vector<int> &blocks, const vector<tuple<int, int>> &idCounts, vector<tuple<int, int>> &freeFromTo)
{
    for (int i = idCounts.size() - 1; i >= 0; i--)
    {

        // for(int& b : blocks) {
        //     cout << b << " ";
        // }
        // cout << endl;

        auto [needSpace, idIdx] = idCounts[i];
        for (tuple<int, int> &fromTo : freeFromTo)
        {
            auto [freeFrom, freeTo] = fromTo;
            if (freeFrom >= idIdx)
            {
                break;
            }
            int isSpace = freeTo - freeFrom + 1;
            if (needSpace <= isSpace)
            {
                for (int j = 0; j < needSpace; j++)
                {
                    blocks[freeFrom + j] = i;
                    blocks[idIdx + j] = -1;
                }
                fromTo = {freeFrom + needSpace, freeTo};
                break;
            }
        }
    }
}

auto puzzleToBlocks(const vector<int> &puzzle)
{
    struct result
    {
        vector<int> blocks;
        vector<tuple<int, int>> idCountsFrom;
        vector<tuple<int, int>> freeFromTo;
    };
    vector<int> block;
    vector<tuple<int, int>> countsFrom;
    vector<tuple<int, int>> freeFromTo;
    int id = 0;

    for (int i = 0; i < puzzle.size(); i++)
    {
        // file blocks
        if (i % 2 == 0)
        {
            vector<int> newBlock(puzzle[i], id);
            block.reserve(block.size() + newBlock.size()); // preallocate memory
            countsFrom.push_back({newBlock.size(), block.size()});
            block.insert(block.end(), newBlock.begin(), newBlock.end());
            id++;
        }
        else
        { // free space
            vector<int> newSpace(puzzle[i], -1);
            block.reserve(block.size() + newSpace.size()); // preallocate memory
            freeFromTo.push_back({block.size(), block.size() + newSpace.size() - 1});
            block.insert(block.end(), newSpace.begin(), newSpace.end());
        }
    }
    return result{block, countsFrom, freeFromTo};
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
    vector<int> puzzle;

    while (getline(f, line))
    {
        for (char c : line)
        {
            puzzle.push_back(c - '0');
        }
    }
    f.close();

    auto [blocksA, idCountsFrom, freeFromTo] = puzzleToBlocks(puzzle);
    vector<int> blocksB(blocksA);
    moveBlocksA(blocksA);
    moveBlocksB(blocksB, idCountsFrom, freeFromTo);

    long long int sumA = 0;
    long long int sumB = 0;
    for (int i = 0; i < blocksA.size(); i++)
    {
        if (blocksA[i] != -1)
        {
            sumA += i * blocksA[i];
        }
    }
    cout << "PART A: " << sumA << endl;

    for (int i = 0; i < blocksB.size(); i++)
    {
        if (blocksB[i] != -1)
        {
            sumB += i * blocksB[i];
        }
    }
    cout << "PART B: " << sumB << endl;

    return 0;
}