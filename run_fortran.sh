#!/bin/bash
# expects two arguments, first for parameter file, second for output file
# copy the parameter file
FILE="s3://mic.urban.org/tpc/simple-tax-model/$1"
echo "Attempting download : $FILE"
# copy parameter file
#for FILE
#do
#  echo " want --- aws s3 cp s3://mic.urban.org/tpc/simple-tax-model/parameterOptions_Standard_1600.csv parameterOptions_Standard_1600.csv"
#  echo " is   --- aws s3 cp $FILE $1"
  #aws s3 cp s3://mic.urban.org/tpc/simple-tax-model/parameterOptions_Standard_1600.csv parameterOptions_Standard_1600.csv
aws s3 cp $FILE $1
#done

#need a little tweak to output file name
OUTNAME="$2.csv"
echo "running fortran"
./fortmodel "$1" "$OUTNAME"
echo "fortran complete"

# copy results
OUTFILE="s3://mic.urban.org/tpc/simple-tax-model/$2.csv"
aws s3 cp $OUTNAME $OUTFILE
