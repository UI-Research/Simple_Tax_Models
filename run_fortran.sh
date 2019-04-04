#!/bin/bash
# expects two arguments, first for parameter file, second for output file
# copy the parameter file
KEY="s3://mic.urban.org/tpc/simple-tax-model/""$1"
echo "Attempting download : $KEY as $1"

for KEY
do
  aws s3 cp "$KEY" "$1"
done

echo "running fortran"
./fortmodel "$1" "$2"
echo "fortran complete"
