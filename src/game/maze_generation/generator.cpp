#include <iostream>
#include <cmath>
#include <ctime>
#include <vector>
#include <stack>
#include <cstdlib>
#include <random>
#include <fstream>
#include <algorithm>
#include <cstring>

using namespace std;

struct Cell
{
    int x, y;
    char type;

    Cell(int x, int y, char type) : x(x), y(y), type(type) {}
};

enum CellType {
    WALL = '#', PATH = ' ', START = 's', END = 'e',
    WALL_file = 'w', PATH_file = 'p'
};

class Maze
{
public:
    Maze(const char* config_file) : generator(random_device{}())
    {
        readSizeFromFile(config_file, width, height);
        grid = vector<vector<Cell>>(height, vector<Cell>(width, Cell(0, 0, CellType::WALL)));
        for (int i = 0; i < height; i++)
        {
            for (int j = 0; j < width; j++)
            {
                grid[i][j] = Cell(j, i, CellType::WALL);
            }
        }
        generateMaze();
        establishStartFinish();
    }

    void saveMazeToFile(const char* fname)
    {
        ofstream File(fname);
        if (!File)
        {
            cerr << "Error opening file" << fname << "\n";
            return;
        }

        File << height << '\n';
        File << width << '\n';

        for (int i = 0; i < height; i++)
        {
            for (int j = 0; j < width; j++)
            {
                char charType = grid[i][j].type;
                if (charType == CellType::WALL)
                {
                    charType = CellType::WALL_file;
                }
                else if (charType == CellType::PATH)
                {
                    charType = CellType::PATH_file;
                }
                File << grid[i][j].x << ' ' << grid[i][j].y << ' ' << charType << '\n';
            }
        }
        File.close();
    }

private:
    vector<vector<Cell>> grid;
    int width, height;
    Cell* start = nullptr;
    Cell* end = nullptr;
    default_random_engine generator;

    void readSizeFromFile(const char* filename, int& width, int& height)
    {
        ifstream file(filename); 
        if(!file.is_open()){
            throw runtime_error("Error opening file" + string(filename));
        }

        if (!(file >> width >> height)) {
            file.close();
            throw runtime_error("Error reading size data from file");
        }

        if (width <= 0 || height <= 0) {
            file.close();
            throw invalid_argument("Width and height must be positive integers");
        }
        file.close();
    }

    void generateMaze()
    {
        stack<Cell*> stack;

        grid[1][1].type = CellType::PATH;
        stack.push(&grid[1][1]);

        while (!stack.empty())
        {
            Cell* curr = stack.top();
            vector<Cell*> neighbor = getNeighbor(curr);
            if (!neighbor.empty())
            {
                uniform_int_distribution<int> dist(0, neighbor.size() - 1);
                Cell* next = neighbor[dist(generator)];
                destroyWall(curr, next);
                next->type = CellType::PATH;
                stack.push(next);
            }
            else
            {
                stack.pop();
            }
        }
    }

    vector<Cell*> getNeighbor(Cell* cell)
    {
        vector<Cell*> neighbor;
        static const int direction[4][2] = { {0, -2}, {-2, 0}, {0, 2}, {2, 0} };

        vector<int> order = { 0, 1, 2, 3 };
        shuffle(order.begin(), order.end(), generator);

        for (int i : order)
        {
            int newX = cell->x + direction[i][0];
            int newY = cell->y + direction[i][1];

            if (newX > 0 && newX < width - 1 && newY > 0 && newY < height - 1 && grid[newY][newX].type == CellType::WALL)
            {
                neighbor.push_back(&grid[newY][newX]);
            }
        }
        return neighbor;
    }

    void establishStartFinish()
    {
        start = &grid[1][1];
        start->type = CellType::START;

        end = &grid[height - 2][width - 2];
        end->type = CellType::END;
    }

    void destroyWall(Cell* a, Cell* b)
    {
        int Xwall = (a->x + b->x) / 2;
        int Ywall = (a->y + b->y) / 2;

        grid[Ywall][Xwall].type = CellType::PATH;
    }
};

extern "C" {
    Maze* Maze_new(const char* config_file) {
        try {
            return new Maze(config_file);
        }
        catch (const exception& e) {
            cerr << "Error creating maze: " << e.what() << endl;
            return nullptr;
        }
        
    }

    void Maze_delete(Maze* maze) {
        delete maze;
    }

    void Maze_saveMazeToFile(Maze* maze, const char* file_name) {
        maze->saveMazeToFile(file_name);
    }
}