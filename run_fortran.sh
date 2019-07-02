#!/bin/bash
# expects two arguments, first for parameter file, second for output file
# copy the parameter file
FILE="s3://your_input_bucket/$1"
echo "Attempting download : $FILE"
# copy parameter file
aws s3 cp $FILE $1
#done

#need a little tweak to output file name
OUTNAME="$2.csv"
echo "running fortran"
./fortmodel "$1" "$OUTNAME"
echo "fortran complete"

# copy results
OUTFILE="s3://your_output_bucket/$2.csv"
aws s3 cp $OUTNAME $OUTFILE
