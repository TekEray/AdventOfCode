#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <queue>

using namespace std;

enum Direction {
  LEFT,
  RIGHT,
  UP,
  DOWN,
  NONE
};

enum Objects {
  WALL,
  START,
  END,
  NOTHING
};

map<enum Direction, pair<int,int>> moveDir = {{LEFT, pair(0,-1)},
                                         {RIGHT, pair(0,1)},
                                         {UP, pair(-1,0)},
                                         {DOWN, pair(1,0)}};

using PQEntry = pair<int, pair<int, enum Direction>>;

pair<int,int> getRowCol(int id, int width)
{
    int row,col;

    row = id / width;
    col = id % width; 

    return pair(row,col);
}

map<pair<int, enum Direction>, int> dijkstra(const vector<vector<enum Objects>> mapMaze, pair<int,int> startPos){

    int width = mapMaze[0].size();
    priority_queue<PQEntry, vector<PQEntry>, greater<>> minHeap;
    
    //init Dist
    map<pair<int, enum Direction>, int> dist;
    for(int x=0; x<mapMaze.size();x++){
        for( int y=0; y < mapMaze[x].size(); y++){
            for(int z = LEFT; z != NONE; z++){
                enum Direction tDir = static_cast<Direction>(z);
                dist[{width * x + y, tDir}] = INT_MAX;
            }
        }
    }
    vector<map<enum Direction, bool>> visited(dist.size(), {{LEFT, false},
                                                        {RIGHT, false},
                                                        {UP, false},
                                                        {DOWN, false}});    

    //startPos
    int startId = width*startPos.first + startPos.second;
    pair<int, enum Direction> startPair = pair(startId, RIGHT);
    dist[startPair] = 0;
    minHeap.push({0, startPair});
    int testSize = dist.size();
    while (!minHeap.empty()) {
        auto [distVal, idDir] = minHeap.top();
        minHeap.pop();
        int id = idDir.first;
        enum Direction direction = idDir.second;
        pair<int,int> rowCol = getRowCol(id, width);

        visited[id][direction] = true;

        int weight;
        for(int j = LEFT; j != NONE; j++){
            enum Direction dir = static_cast<Direction>(j);
            if (dir == direction){
                weight = 1;
            }else {
                weight = 1001;
            }
            int nextWeight = distVal + weight;
            pair<int,int> nextRowCol = pair(rowCol.first + moveDir[dir].first, rowCol.second + moveDir[dir].second);
            int nextId = width*nextRowCol.first + nextRowCol.second;
            pair<int, enum Direction> nextIdDir = pair(nextId,dir);
            if (mapMaze[nextRowCol.first][nextRowCol.second] != WALL && !visited[nextId][dir] && nextWeight < dist[nextIdDir]){
                dist[nextIdDir] = nextWeight;
                minHeap.push({nextWeight, nextIdDir});
            }
        }
    }
    return dist;
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
    vector<vector<enum Objects>> mapMaze;
    bool findEndl = false;
    int idxMapX = 0;
    pair<int,int> initStartPos;
    pair<int,int> initEndPos;
    while (getline(f, line))
    {
        vector<enum Objects> tmpLine;
        int idxMapY = 0;
        for (const char &obj : line){
            switch (obj)
            {
            case '#':
                tmpLine.push_back(WALL);
                break;
            case 'S':
                tmpLine.push_back(START);
                initStartPos = pair(idxMapX,idxMapY);
                break;
            case '.':
                tmpLine.push_back(NOTHING);
                break;
            case 'E':
                tmpLine.push_back(END);
                initEndPos = pair(idxMapX,idxMapY);
                break;
            default:
                break;
            }
            idxMapY++;
        }
        mapMaze.push_back(tmpLine);
        idxMapX++;
    }
    f.close();

    // PART A
    map<pair<int, enum Direction>, int> dist = dijkstra(mapMaze, initStartPos);
    int endId = mapMaze[0].size()*initEndPos.first + initEndPos.second;
    
    int minA = INT_MAX;
    for(int z = LEFT; z != NONE; z++){
        enum Direction tDir = static_cast<Direction>(z);
        pair<int, enum Direction> tmpPair = pair(endId, tDir);
        if (dist[tmpPair] < minA){
            minA = dist[tmpPair];
        }
    }
    cout << "PART A: " << minA << endl;

    return 0;
} 