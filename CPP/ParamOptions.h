#pragma once

#include <string>

class ParamOptions {
public:
  ParamOptions(){};
  ~ParamOptions(){};

private:
  std::string label;
  double value;

public:
  void extractVarsFromLine(const std::string& inputLine);

  std::string getLabel() { return label; }
  double getValue(){ return value; }

  void setLabel(std::string newLabel);
  void setValue(double newValue);
};
