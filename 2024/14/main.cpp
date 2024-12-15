#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_set>

using namespace std;

int mod(int a, int b){
    return ((a % b) + b) % b;
}

void printRaster(const vector<pair<int,int>> pos, pair<int,int> roomSize)
{
    vector<vector<char>> grid(roomSize.second, vector<char>(roomSize.first, '.'));

    // Punkte im Raster markieren
    for (const auto& point : pos) {
        int x = point.first;  
        int y = point.second; 
        grid[y][x] = '*'; 
    }

    // Raster ausgeben
    for (const auto& row : grid) {
        for (const auto& cell : row) {
            cout << cell;
        }
        cout << endl;
    }
}

vector<pair<int,int>> posAfterSec(const vector<pair<int,int>> pos, const vector<pair<int,int>> vel,  int t, pair<int,int> space )
{
    vector<pair<int,int>> newPos(pos);
    for(int i=0; i<t; i++){
        for (int i = 0; i < newPos.size(); i++) {
            newPos[i] = pair(mod((newPos[i].first + vel[i].first), space.first), mod((newPos[i].second + vel[i].second), space.second));
        }
    }
    return newPos;
}

string pointToString(int x, int y) {
    return to_string(x) + "," + to_string(y);
}

int findSymmetrieCount(const vector<pair<int,int>> pos, pair<int,int> space){
    unordered_set<string> pointSet;
    for (const auto& point : pos) {
        pointSet.insert(pointToString(point.first, point.second));
    }

    int maxSymmetricPoints = 0;
    int bestSymmetryAxis = 0;

    // Überprüfe mögliche vertikale Symmetrieachsen
    for (int k = 0; k < space.first; ++k) { // Achse bei x = k testen
        int symmetricCount = 0;

        for (const auto& point : pos) {
            int x = point.first;
            int y = point.second;

            // Symmetrischen Punkt in Bezug auf Achse x = k berechnen
            int symmetricX = 2 * k - x;

            // Prüfen, ob der symmetrische Punkt existiert
            if (pointSet.count(pointToString(symmetricX, y))) {
                symmetricCount++;
            }
        }

        // Maximale Anzahl symmetrischer Punkte aktualisieren
        if (symmetricCount > maxSymmetricPoints) {
            maxSymmetricPoints = symmetricCount;
            bestSymmetryAxis = k;
        }
    }

    return maxSymmetricPoints;
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
    vector<pair<int,int>> positions;
    vector<pair<int,int>> posAfterTime;
    vector<pair<int,int>> velocities;
    while (getline(f, line))
    {
        int px, py, vx, vy;

        // Parsing der Zeile
        if (sscanf(line.c_str(), "p=%d,%d v=%d,%d", &px, &py, &vx, &vy) == 4) {
            positions.emplace_back(px, py);
            velocities.emplace_back(vx, vy);
        }
    }
    f.close();

    pair<int,int> roomSize = pair(101,103);
    int midX = (roomSize.first / 2);
    int midY = (roomSize.second / 2);
    posAfterTime = posAfterSec(positions, velocities, 100, roomSize);
    int topLeft = 0;
    int topRight = 0;
    int bottomLeft = 0;
    int bottomRight = 0;
    for (const auto& pos : posAfterTime) {
        if (pos.first < midX && pos.second < midY){
            topLeft++;
        }else if (pos.first > midX && pos.second < midY){
            topRight++;
        }else if (pos.first < midX && pos.second > midY){
            bottomLeft++;
        }else if (pos.first > midX && pos.second > midY){
            bottomRight++;
        }
    }

    cout << "PART A: " << topLeft * topRight * bottomLeft * bottomRight << endl;

    int tCounter = 0;
    vector<pair<int,int>> newPos(positions);
    int maxSymmetricPoints = findSymmetrieCount(newPos, roomSize);
    while (maxSymmetricPoints < 350){
        newPos = posAfterSec(newPos, velocities, 1, roomSize);
        maxSymmetricPoints = findSymmetrieCount(newPos, roomSize);
        tCounter++;
    }
    printRaster(newPos, roomSize);
    cout << "PART B: " << tCounter << endl;

    return 0;
} 