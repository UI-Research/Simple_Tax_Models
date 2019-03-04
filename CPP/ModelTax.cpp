/*********
Toy model. Done in C++
Main entry point.

Jessica A Kelly
jkelly@urban.org

**********/

#include <iostream>
#include <iomanip>
#include <iostream>
#include <fstream>
#include <string>
#include "TaxFiler.h"
#include "ParamOptions.h"
#include "ModelTax.h"
using namespace std;

// Description: Main function to control program flow.
//  Calls read_input, do_regressions and write_output
//  offload these functions to a class
int main(int argc, char* argv[]){
   cout << "C++-based Simple Tax Public Model Example" << endl;
   // create the model
   // could pass as arguments instead
   model = new CppModel("..//data//Demo.csv", "parameterOptions.csv", "output.csv");
   // make sure we are mindful of looping!
   // we could run (but it has more loops than we want):
   // model->readAllFile();
   // model->readParams();
   // model->testCalc();
   // model->writeAllOutput();

   // more efficient with loops
   // read parameters first since will need to know all of these up-front
   model->readParams();

   // begin looping over records as they are read.
   // but the minute we need to know something across all tax filers, this
   // will break down and we need to switch to the above
   ifstream iFile(model->inputFile.c_str());
   model->oFile.open(model->outFile.c_str());
   // write header (could make function)
   model->oFile << "unitId" <<","
     << "itemized" << ","
     << "salary" << ","
     << "filingStatus" << ","
     << "weight" << ","
     << "tax"
     << endl;
   if (iFile.fail()) {
     // do something, this is an error.
     cout << "Failed to open "<< model->inputFile << endl;
   }
   else {
     string FullLine;
     bool firstLine = true; // can use if we have a header.
     long count = 0;
     while (!iFile.eof()) {
       getline(iFile, FullLine);
       //cout << "read a line: "<<FullLine << endl;
       // could put test for header record here.
       firstLine = false;
       count++;
       if (FullLine != "") {
           model->filer = new TaxFiler();
           model->filer->extractVarsFromLine(FullLine);

       }// end full line is not blank

       // after read, then do some math
       // set up to call calcTax
       double salary = model->filer->getSalary();
       double itemized = model->filer->getItemized();
       // if we don't find these options in the parameter file, just set default
       string findIt ="STANDARD";
       double standard = model->findValue(findIt);
       if (standard == -999999) standard = 1000;
       findIt = "RATE";
       double rate = model->findValue(findIt);
       if (rate == -999999) rate = 0.1;
       findIt = "EXEMPT";
       double exempt = model->findValue(findIt);
       if (exempt == -999999) exempt = 1000;
       int filingStatus = model->filer->getFilingStatus();
       // calculate tax
       double tax = model->filer->calcTax(salary, itemized, standard, rate, exempt, filingStatus);
       model->filer->setTestOutputVariable(tax);
       // then we can output
       // could be more elegant here, but not needed.
       model->oFile << model->filer->getUnitId() <<","
         << model->filer->getItemized() << ","
         << model->filer->getSalary() << ","
         << model->filer->getFilingStatus() << ","
         << model->filer->getWeight() << ","
         << model->filer->getTestOutputVariable()
         << endl;
       // add a counter that prints every 10,000 recs read
       if(count%10000 == 0) {
         cout << count << " observations processed." << endl;
       }
     }// end loop over each line
     cout << count << " total observations processed. "<< endl;
     delete model->filer;
   } // end else read file ok

   iFile.close();
   model->oFile.close();
   cout << "output file " << model->outFile.c_str() << " written." << endl;
   cout << "processing complete!" << endl;
   delete model;

   return 0;
}

// all CppModel class below
CppModel::CppModel(const string& inputFilename, const string& inOptsFilename, const string& outputFile):
inputFile(inputFilename), inOpts(inOptsFilename), outFile(outputFile) {
  // any other initialization
}
// let the compiler do it;
//CppModel::~CppModel() {
// delete filers requires a loop
// delete opts requires a loop
//}

// Description: Reads the input file, all in one go.
void CppModel::readAllFile() {
  ifstream iFile(inputFile.c_str());
  if (iFile.fail()) {
    // do something, this is an error.
    cout << "Failed to open "<< inputFile << endl;
  }
  else {
    string FullLine;
    bool firstLine = true; // can use if we have a header.
    long count = 0;
    while (!iFile.eof()) {
      getline(iFile, FullLine);
      //cout << "read a line: "<<FullLine << endl;
      // could put test for header record here.
      firstLine = false;
      if (FullLine != "") {
          try {
            filers.push_back(new TaxFiler());
          }
          catch (exception& oe) {
            cout << "Error TaxFiler " << oe.what() << " count = " << count << endl;
          }
          catch (...)
          {
            cout << "Unknown Error reading tax filer input " << endl;
          }
          int last = filers.size() - 1;
          filers[last]->extractVarsFromLine(FullLine);
        }// end full line is not blank
    }// end loop over each line
  } // end else read file ok

  iFile.close();
}


// Description: reads parameter options and holds those in an options vector.
void CppModel::readParams() {
  ifstream iFile(inOpts.c_str());
  if (iFile.fail()) {
    // do something, this is an error.
    cout << "Failed to open "<< inOpts << endl;
  }
  else {
    string FullLine;
    bool firstLine = true;
    long count = 0;
    while (!iFile.eof()) {
      getline(iFile, FullLine);
      //cout << "read a line: "<<FullLine << endl;
      firstLine = false;
      if (FullLine != "") {
          try {
            opts.push_back(new ParamOptions());
          }
          catch (exception& oe) {
            cout << "Error ParamOptions " << oe.what() << " count = " << count << endl;
          }
          catch (...)
          {
            cout << "Unknown Error reading parameter options input " << endl;
          }
          int last = opts.size() - 1;
          opts[last]->extractVarsFromLine(FullLine);
      }// end full line is not blank
    }// end loop over each line
  } // end else read file ok

  iFile.close();
}

// Description: Use a something from opts and filers
void CppModel::testCalc() {
  string findIt ="RATES1";
  double rates = findValue(findIt);
  if (rates == -999999) rates = 1;
  for(int i =0; i<filers.size(); i++) {
    double testMod = filers[i]->getSalary() * rates;
    filers[i]->setTestOutputVariable(testMod);
    //cout << "doing test calculation and testMod = " << testMod << endl;

  }
}

// Description: writes output all at once.
void CppModel::writeAllOutput(){
  oFile.open(outFile.c_str());
  for(int i =0; i<filers.size(); i++) {
    oFile << filers[i]->getUnitId() <<"," << filers[i]->getTestOutputVariable() <<endl;
  }
  oFile.close();
}

// Description: finds a value corresponding to a label
//  assuming there are only doubles that are values.
//
// Remarks: returns -999999 if cannot find.
double CppModel::findValue(string& label){
  double retValue = -999999;
  for (int i = 0; i< opts.size(); i++) {
    if(opts[i]->getLabel() == label) {
      retValue = opts[i]->getValue();
    }
  }
  return retValue;
}
