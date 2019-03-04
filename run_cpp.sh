#!/bin/bash
echo "running cpp"
./cppmodel
echo "cpp complete"
echo "running summarize"
python ../summarize/create_summary_tables.py output.csv
echo "summarize complete"
#note that gets written to the directory we are in now
#will need to get copied somewhere to save
cat summary_output.csv
