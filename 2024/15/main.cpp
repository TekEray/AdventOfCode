#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

enum Moves {
  LEFT,
  RIGHT,
  UP,
  DOWN
};

enum Objects {
  WALL,
  BOX,
  ROBOT,
  NOTHING
};

enum ObjectsB {
  WALLB,
  BOXLB,
  BOXRB,
  ROBOTB,
  NOTHINGB
};

map<enum Moves, pair<int,int>> moveDir = {{LEFT, pair(0,-1)},
                                         {RIGHT, pair(0,1)},
                                         {UP, pair(-1,0)},
                                         {DOWN, pair(1,0)}};

pair<int,int> initRobotPos;
pair<int,int> robotPos;

void moveObject(int objectX, int objectY, enum Moves move, vector<vector<enum Objects>> &map){
    int newX = objectX + moveDir[move].first;
    int newY = objectY + moveDir[move].second;
    if(newX < 0 || newX >= map.size() || newY < 0 || newY >= map[newX].size() || map[newX][newY] == WALL){
        return;
    }
    if (map[newX][newY] == BOX){
        moveObject(newX, newY, move, map);
    }
    if (map[newX][newY] == NOTHING){
        map[newX][newY] = map[objectX][objectY];
        map[objectX][objectY] = NOTHING;
        if (map[newX][newY] == ROBOT){
            robotPos = pair(newX, newY);
        }
    }
}

bool checkMoveB(int objectX, int objectY, enum Moves move, vector<vector<enum ObjectsB>> &map){
    int newX = objectX + moveDir[move].first;
    int newY = objectY + moveDir[move].second;
    if(newX < 0 || newX >= map.size() || newY < 0 || newY >= map[newX].size() || map[newX][newY] == WALLB){
        return false;
    }
    if (map[newX][newY] == NOTHINGB){
        return true;
    }
    if (map[newX][newY] == BOXLB && (move == UP || move == DOWN)){
        return checkMoveB(newX, newY, move, map) && checkMoveB(newX, newY+1, move, map);
    }
    if (map[newX][newY] == BOXRB && (move == UP || move == DOWN)){
        return checkMoveB(newX, newY, move, map) && checkMoveB(newX, newY-1, move, map);
    }
    if (map[newX][newY] == BOXLB && move == RIGHT){
        return checkMoveB(newX, newY+1, move, map);
    }
    if (map[newX][newY] == BOXRB && move == LEFT){
        return checkMoveB(newX, newY-1, move, map);
    }
    return false;
}

void moveObjectB(int objectX, int objectY, enum Moves move, vector<vector<enum ObjectsB>> &map){
    int newX = objectX + moveDir[move].first;
    int newY = objectY + moveDir[move].second;

    if ((move == UP || move == DOWN)){
        if (map[newX][newY] == BOXLB){
            moveObjectB(newX, newY, move, map);
            moveObjectB(newX, newY+1, move, map);
        }
        if (map[newX][newY] == BOXRB){
            moveObjectB(newX, newY, move, map);
            moveObjectB(newX, newY-1, move, map);
        } 
    }
    if ((move == LEFT || move == RIGHT) && (map[newX][newY] == BOXLB || map[newX][newY] == BOXRB)){
        moveObjectB(newX, newY, move, map);
    }
    if (map[newX][newY] == NOTHINGB){
        map[newX][newY] = map[objectX][objectY];
        map[objectX][objectY] = NOTHINGB;
        if (map[newX][newY] == ROBOTB){
            robotPos = pair(newX, newY);
        }
    }
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
    vector<vector<enum Objects>> mapWarehouse;
    vector<vector<enum ObjectsB>> mapWarehouseB;
    vector<enum Moves> moveAttempts;
    bool findEndl = false;
    int idxMapX = 0;
    while (getline(f, line))
    {
        if (line.empty())
        {
            findEndl = true;
            continue;
        }
        if(!findEndl){
            vector<enum Objects> tmpLine;
            vector<enum ObjectsB> tmpLineB;
            int idxMapY = 0;
            for (const char &obj : line){
                switch (obj)
                {
                case '#':
                    tmpLine.push_back(WALL);
                    
                    tmpLineB.push_back(WALLB);
                    tmpLineB.push_back(WALLB);
                    break;
                case '@':
                    tmpLine.push_back(ROBOT);
                    
                    tmpLineB.push_back(ROBOTB);
                    tmpLineB.push_back(NOTHINGB);
                    initRobotPos = pair(idxMapX,idxMapY);
                    break;
                case '.':
                    tmpLine.push_back(NOTHING);
                    
                    tmpLineB.push_back(NOTHINGB);
                    tmpLineB.push_back(NOTHINGB);
                    break;
                case 'O':
                    tmpLine.push_back(BOX);
                    
                    tmpLineB.push_back(BOXLB);
                    tmpLineB.push_back(BOXRB);
                    break;
                default:
                    break;
                }
                idxMapY++;
            }
            mapWarehouse.push_back(tmpLine);
            mapWarehouseB.push_back(tmpLineB);
            idxMapX++;
        }else{
            for (const char &move : line){
                switch (move)
                {
                case '<':
                    moveAttempts.push_back(LEFT);
                    break;
                case '>':
                    moveAttempts.push_back(RIGHT);
                    break;
                case '^':
                    moveAttempts.push_back(UP);
                    break;
                case 'v':
                    moveAttempts.push_back(DOWN);
                    break;
                default:
                    break;
                }
            }
        }
    }
    f.close();

    // PART A
    robotPos = pair(initRobotPos.first, initRobotPos.second);
    for( const auto &move : moveAttempts){
        moveObject(robotPos.first,robotPos.second, move, mapWarehouse);
    }

    int sumA = 0;
    for(int i = 0; i < mapWarehouse.size(); i++){
        for( int j = 0; j < mapWarehouse[i].size(); j++){
            if(mapWarehouse[i][j] == BOX){
                sumA +=  (100*i) + j;
            }
        }
    }
    cout << sumA << endl;

    // PART B
    robotPos = pair(initRobotPos.first, initRobotPos.second * 2);
    for( const auto &move : moveAttempts){
        if(checkMoveB(robotPos.first,robotPos.second, move, mapWarehouseB)){
            moveObjectB(robotPos.first,robotPos.second, move, mapWarehouseB);
        }
    }

    int sumB = 0;
    for(int i = 0; i < mapWarehouseB.size(); i++){
        for( int j = 0; j < mapWarehouseB[i].size(); j++){
            if(mapWarehouseB[i][j] == BOXLB){
                sumB +=  (100*i) + j;
            }
        }
    }
    cout << sumB << endl;

    return 0;
} 