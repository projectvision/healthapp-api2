/*
 * A utility script to parse crime spot data
 *
 */
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <cmath>
#include <map>

using namespace std;

double round(double x, unsigned int precision) {
  long long unsigned int mult = pow(10, precision);
  x = x * pow(10, precision);
  x += x < 0 ? -0.5 : 0.5;
  x = int(x) * 1.0 / mult;
  return x;
}

// taken from http://stackoverflow.com/questions/1120140/how-can-i-read-and-parse-csv-files-in-c
void ParseCSV(const string& csvSource, vector<vector<string> >& lines) {
   bool inQuote(false);
   bool newLine(false);
   string field;
   lines.clear();
   vector<string> line;

   string::const_iterator aChar = csvSource.begin();
   while (aChar != csvSource.end())
   {
      switch (*aChar)
      {
      case '"':
         newLine = false;
         inQuote = !inQuote;
         break;

      case ',':
         newLine = false;
         if (inQuote == true)
         {
            field += *aChar;
         }
         else
         {
            line.push_back(field);
            field.clear();
         }
         break;

      case '\n':
      case '\r':
         if (inQuote == true)
         {
            field += *aChar;
         }
         else
         {
            if (newLine == false)
            {
               line.push_back(field);
               lines.push_back(line);
               field.clear();
               line.clear();
               newLine = true;
            }
         }
         break;

      default:
         newLine = false;
         field.push_back(*aChar);
         break;
      }

      aChar++;
   }

   if (field.size())
      line.push_back(field);

   if (line.size())
      lines.push_back(line);
}


int main(int argc, char *argv[]) {
  //cout << "Reading file: " << argv[1] << endl;

  ifstream inFile;
  inFile.open(argv[1]);

  stringstream strStream;
  strStream << inFile.rdbuf();
  string str = strStream.str();

  vector<vector<string> > lines;
  ParseCSV(str, lines);
  lines.erase(lines.begin()); //remove the header line

  float lat, lng;
  const unsigned int precision = 1;

  map<pair<float,float>, int> crime_map;

  for (auto &row : lines) {
    lat = round(stod(row[3]), precision);
    lng = round(stod(row[4]), precision);
    pair<float, float> position = make_pair(lat, lng);
    //cout << lat << "," << lng << endl;
    if (crime_map.find(position) == crime_map.end() ) {
      crime_map[position] = 1;
    }
    else {
      crime_map[position]++;
    }

  }

  for (auto &pos : crime_map) {
    cout << pos.first.first << "," << pos.first.second << "," << pos.second << endl;
  }

}
