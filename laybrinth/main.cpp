//author shreyas2000

#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <fstream>
#include <string>

using namespace std;

vector<vector<int>> path;
vector<vector<int>> weights;
vector<vector<int>> visited;

void set_all(){
   
    visited = path;
    weights = path;
   
    for (int i = 0; i < path.size(); i++){
        for (int j = 0; j < path[0].size(); j++){
            weights[i][j] = 0;
        } 
    } 
}


vector<int> algo(){
  
   int maxi = 100;
   int max_row = 0;
   int max_col = 0;

   for(int i=0; i<path.size(); i++){
      for(int j=0; j<path[0].size(); j++){
        if(path[i][j])  // the point is available or a wall
        {  // the point has the max value and not visited
            if ( (weights[i][j]>maxi || maxi==100) && (visited[i][j]!=0) )  
            {
               maxi = weights[i][j];
               max_row = i;
               max_col = j;
            }
        }
    }
}
    return vector<int>{max_row, max_col};
}


void neighbours(int i, int j)
{
   visited[i][j] = 0;
   for(int x=-1; x<=1; x+=2)
   {  // assign weights to up and down
      if (i+x>=0 && i+x<5 && path[i+x][j] && visited[i+x][j] != 0)
      {
         weights[i+x][j] = weights[i][j] + 1;
      }
      if (j+x>=0 && j+x<7 && path[i][j+x] && visited[i][j+x]!= 0)
      {  //assign weights to right and left
         weights[i][j+x] = weights[i][j] + 1;
      }
   }
}
   
   
bool check(vector<vector<int>> v)
{
    /*check if all possible points were visited*/
    for (int i=0; i<v.size(); i++){
        for (int j = 0; j < v[0].size(); j++) {
            if (path[i][j] == 1 && v[i][j] ==1) {
                return false;
            }
        }
    }
    return true;
}
   
void printvector(vector<vector<char>> v){
    /* print matrix v*/
    for (int i = 0; i < v.size(); i++) {
        for (int j = 0; j < v[0].size(); j++) {
            cout << v[i][j];
        }
        cout << '\n';
    }
}


vector<vector<int>> read_file(string s){
    /* param s: name of the file
       return way: 2D vector representing available points
       '#' --> 0   and  '.' --> 1
    */
    ifstream file(s);
    string line;
    
    vector<int> one;
    vector<vector<int>> way;
    while(getline(file, line)){
        for (int i = 0; i < line.size(); i++)
        {
            if (line[i] == '#')
            {
                one.push_back(0);
            }
            else
            {
                one.push_back(1);
            }
        }
        way.push_back(one);
        one.clear(); 
    }
    return way;
}


vector<vector<char>> back2(vector<vector<int>> v){
    /* back track to display the world */
    vector<int> maxe;
    vector<vector<char>> fin;
    vector<char> w;
    //create matrix with # and . 
    for (int i = 0; i < v.size(); i++)
    {
        for (int j = 0; j < v[0].size(); j++)
        {
            if (path[i][j] == 1)
            {
                w.push_back('.');
            }
            else
            {
                w.push_back('#');
            }
        }
        fin.push_back(w);
        w.clear();
    }

    // max element row, col and value 
    auto it = max_element(v.begin(), v.end());
    int row = it - v.begin();
    auto it2 = max_element(v[row].begin(), v[row].end());
    int col = (it2 - v[row].begin());
    int emax = *it2;

    cout<<emax+1<<endl; // the value of the steps
    fin[row][col] = '0' + emax;
   
    // from the max to 0 assign the values in fin matrix
    while (emax>0)
    {
        emax --;
        for(int x=-1; x<=1; x+=2)
        {
            if (v[row+x][col]==emax && row+x>=0 && row+x<5)
            {
                fin[row+x][col] = '0' + emax;
                row = row+x;
                break;
            }
            else if (v[row][col+x]==emax && col+x>=0 && col+x<7)
            {
                fin[row][col+x] = '0' + emax;
                col = col+x;
                break;
            }
        }
           
    }
    return fin;
}


int main()
{
    path = read_file("input.txt"); //read the data from data.txt
    set_all();  // initize the weights with zeros
    
    vector<int> pos;
    bool done = false;
    while (! done)
    {
        //find heighst not visited
        vector<int> pos = algo();    
        // assign weights to neighbours
        neighbours(pos[0], pos[1]);
        done = check(visited);
    }
    vector<vector<char>> f = back2(weights);
    printvector(f);     //display the vectors
    return 0;
}
