#!/bin/bash
# expects two arguments, first for parameter file, second for output file
# copy the parameter file
KEY="s3://mic.urban.org/tpc/simple-tax-model/""$1"
echo "Attempting download : $KEY"
# copy parameter file
for KEY
do
  aws s3 cp $KEY /param
done
PARAMETER_PATH="/param/$1"

echo "running fortran"
./fortmodel "$PARAMETER_PATH" "$2"
echo "fortran complete"

# copy results
