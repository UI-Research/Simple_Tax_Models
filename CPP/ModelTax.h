#pragma once
#include <string>
#include <vector>
class CppModel;

// functions
int main(int argc, char* argv[]);
CppModel* model;

class CppModel {
public:
  CppModel(const std::string& inputFilename, const std::string& inOptsFilename, const std::string& outputFile);
  std::string inputFile;
  std::string inOpts;
  std::string outFile;
  std::ofstream oFile;
  std::vector <TaxFiler *>filers;
  std::vector <ParamOptions *>opts;
  TaxFiler* filer;
  void readFile() {};
  void readAllFile();
  void readParams();
  void testCalc();
  void writeAllOutput();
  void writeOutput(){};
  double findValue(std::string& label);
};
