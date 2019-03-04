/*
*/

#pragma once

#include <string>

class TaxFiler {
private:
  // input variables
  std::string unitId;
  double itemized;
  double salary;
  int filingStatus;
  double weight;

  // calculated variables
  int bracket;
  double testOutputVariable;

public:
  TaxFiler();
  ~TaxFiler() {};
  void clear();
  void extractVarsFromLine(const std::string& inputLine);

  // get functions
  // input variables
  std::string getUnitId() { return unitId; }
  double getItemized() { return itemized; }
  double getSalary() { return salary; }
  double getTestOutputVariable() { return testOutputVariable; }
  int getFilingStatus() { return filingStatus; }
  double getWeight() { return weight; }
  // calculated variables
  int getBracket() { return bracket; }


  // set functions
  // input variables
  void setUnitId(std::string newUnitId);
  void setItemized(double newItemized);
  void setSalary(double newSalary);
  void setFilingStatus(int newFilingStatus);
  void setWeight(double newWeight);
  // calculated variables
  void setBracket(int newBracket);
  double calcTax(double salary, double itemized, double standard, double rate, double exempt, int filingStatus);
  void setTestOutputVariable(double newTestOutputVariable);

};
