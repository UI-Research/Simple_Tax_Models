#!/bin/bash
# expects two arguments, first for parameter file, second for output file
# copy the parameter file
KEY=s3://mic.urban.org/tpc/simple-tax-model/parameterOptions_Standard_1600.csv
echo "Attempting download : $KEY"
# copy parameter file
for KEY
do
  aws s3 ls s3://mic.urban.org/tpc/simple-tax-model/
  aws s3 cp $KEY parameterOptions_Standard_1600.csv
done


echo "running fortran"
./fortmodel "$1" "$2"
echo "fortran complete"

# copy results
