/*
Tax Filer variables and extract function
*/

#include <string>
#include <sstream>
#include <iostream>


#include "TaxFiler.h"

using namespace std;

// Constructor
TaxFiler::TaxFiler() {
  //any global variable initialization needed here.
}

// set functions
// input variables
void TaxFiler::setUnitId(string newUnitId) {
  unitId = newUnitId;
}
void TaxFiler::setItemized(double newItemized) {
  itemized = newItemized;
}
void TaxFiler::setSalary(double newSalary) {
  salary = newSalary;
}
void TaxFiler::setFilingStatus(int newFilingStatus) {
  filingStatus = newFilingStatus;
}
void TaxFiler::setWeight(double newWeight) {
  weight = newWeight;
}
// calculated variables
void TaxFiler::setBracket(int newBracket) {
  bracket = newBracket;
}
void TaxFiler::setTestOutputVariable(double newTestOutputVariable) {
  testOutputVariable = newTestOutputVariable;
}
// Description: Calculates tax in a very simple manner.
double TaxFiler::calcTax(double salary, double itemized, double standard, double rate, double exempt, int filingStatus){
  double tax = 0.0;
  tax = rate *(salary - max(itemized, standard) - 1000 * (1 + filingStatus));
  return tax;

}


// Description: Clears all the values from TaxFiler
void TaxFiler::clear() {
  setUnitId("");
  setItemized(0.0);
  setSalary(0.0);
  setFilingStatus(0);
  setBracket(0);
  setTestOutputVariable(0.0);
}

// Description: Extracts variables from a single line of the input file
//
// Remarks: Not the most elegant way to do it, but it will work for now.
//
// Arguments:
//   inputLine: the line from the input data
void TaxFiler::extractVarsFromLine(const string& inputLine){
  stringstream strm(inputLine);
  string temp;

  getline(strm, temp, ',');
  setUnitId(temp);

  getline(strm, temp, ',');
  // convert to double
  double doubleTemp = stod(temp);

  setItemized(doubleTemp);

  getline(strm, temp, ',');
  // convert to double
  doubleTemp = stod(temp);
  setSalary(doubleTemp);

  getline(strm, temp, ',');
  // convert to int
  double intTemp = stoi(temp);
  setFilingStatus(intTemp);

  getline(strm, temp, ',');
  // convert to double
  doubleTemp = stod(temp);
  setWeight(doubleTemp);
}
