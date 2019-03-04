/*
Parameter options file read and save
*/

#include <string>
#include <sstream>

#include "ParamOptions.h"

using namespace std;


// set functions
// input variables
void ParamOptions::setLabel(string newLabel) {
  label = newLabel;
}
void ParamOptions::setValue(double newValue) {
  value = newValue;
}

// Description: Extracts variables from a single line of the input file
//
// Remarks: Not the most elegant way to do it, but it will work for now.
//
// Arguments:
//   inputLine: the line from the input data
void ParamOptions::extractVarsFromLine(const string& inputLine){
  stringstream strm(inputLine);
  string temp;

  getline(strm, temp, ',');
  setLabel(temp);

  getline(strm, temp, ',');
  double doubleTemp = stod(temp);
  setValue(doubleTemp);
}
