#python3
#
# Jessica A Kelly
# The Urban Institute
# jkelly@urban.org

# example usage: python3 create_summary_tables.py ../CPP/output.csv

#import csv
import pandas as pd
import os
import argparse
import sys
import csv


# set up arguments to send at command line.
# input is a required argument. if need optional, example is below
def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""

    parser = argparse.ArgumentParser(description='Description of your app.')
    parser.add_argument('input',
                    help='Path to the input file.')
    #parser.add_argument('--outputDirectory',
    #                help='Path to the output.')
    return parser

# load data into dataframe
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# calculate salary bins and return the binned results
def group_by_salary(df):
    #group continuous salary into defined bins
    levels = [min(df["salary"]), 400, 7000, 50000, 93000, max(df["salary"])]
    labels = ["salary <= 400", "400 < salary <= 7,000", "7,000 < salary <= 50,000",
            "50,000 < salary <= 93,000", "salary > 93,000"]
    return pd.cut(df["salary"], bins=levels, labels=labels, include_lowest = True)



# main function
if __name__ == "__main__":
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    if os.path.exists(parsed_args.input):
       PATH = parsed_args.input

    # load and do some initial calculations we need to use later
    df = load_data(PATH)
    df["wgtTax"] = df["tax"] * df["weight"]
    df["avgTax"] = df["tax"] / df["salary"]

    # total tax revenue
    totalTaxRev = df["wgtTax"].sum()
    #print(totalTaxRev)

    # group continuous salary into defined bins
    df["binned"] = group_by_salary(df)
    # and then add up average tax over the bins
    dfavg = df["avgTax"].groupby(df.binned).sum()
    #print(dfavg)

    # then the top decile >140000
    top_decile = df.loc[df["salary"] > 14000, "avgTax"].sum()
    #print(top_decile)
    # and top one percent, over 475000
    top_one_perc = df.loc[df["salary"] > 475000, "avgTax"].sum()
    #print (top_one_perc)

    # clean this up? use loop to add the labels for the dfavg?
    results = {"total tax revenue": totalTaxRev,
        "salary < 400": dfavg[0],
        "400 < salary <= 7,000": dfavg[1],
        "7,000 < salary <= 50,000": dfavg[2],
        "50,000 < salary <= 93,000": dfavg[3],
        "salary > 93,000": dfavg[4],
        "top decile": top_decile,
        "top one percent": top_one_perc}

    #print(results)

    #with open('summary_output.csv', 'w') as f:
    #    writer = csv.writer(f)
    #    for key, value in results.items():
    #        writer.writerow([key, value])
    # this does the above in one line.
    pd.DataFrame.from_dict(data=results, orient='index').to_csv('summary_output.csv', header=False)
