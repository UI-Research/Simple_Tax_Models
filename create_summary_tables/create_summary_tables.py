#python3
#
# Jessica A Kelly
# The Urban Institute
# jkelly@urban.org

import boto3
import pandas as pd
from io import StringIO
from io import BytesIO
import sys
import csv
import os

s3 = boto3.client('s3')

# Description: calculate salary bins and return the binned results
def group_by_salary(df):
    #group continuous salary into defined bins
    levels = [min(df["salary"]), 400, 7000, 50000, 93000, max(df["salary"])]
    labels = ["salary <= 400", "400 < salary <= 7,000", "7,000 < salary <= 50,000",
            "50,000 < salary <= 93,000", "salary > 93,000"]
    return pd.cut(df["salary"], bins=levels, labels=labels, include_lowest = True)

# Description: loads the input_file and does some simple calculations
# returns results dict which is used in the lamdba_handler
def run_summarize(input_file):

    # load and do some initial calculations we need to use later
    df = pd.read_csv(input_file)
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

    #
    results = {"total tax revenue": totalTaxRev,
        "salary < 400": dfavg[0],
        "400 < salary <= 7,000": dfavg[1],
        "7,000 < salary <= 50,000": dfavg[2],
        "50,000 < salary <= 93,000": dfavg[3],
        "salary > 93,000": dfavg[4],
        "top decile": top_decile,
        "top one percent": top_one_perc}

    return results
    #print(results)

# Description: main lambda function
# reads from the S3 bucket, calls run_summarize and then sets up filename and
# writes output to the output S3 location
def lambda_handler(event, context):
    # get s3 bucket and object key from trigger
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    obj = s3.get_object(Bucket=bucket, Key=key)

    # set arguments for summarize
    input_file = BytesIO(obj['Body'].read())
    out = run_summarize(input_file)
    csv_buffer = StringIO()
    #out.to_csv(csv_buffer)
    pd.DataFrame.from_dict(data=out, orient='index').to_csv(csv_buffer, header=False)

    # need a second bucket to write out to
    target_bucket = str(os.environ['TARGET_BUCKET'])
    #target_bucket = "yourbucket"
    s3_resource = boto3.resource('s3')
    # get the portion of the file that contains the output.csv filename
    # if you have a bucket that is more complex with a subdirectory inside
    # this is completely necessary. For the simple case, where there are
    # no / in the string, it will just be the name.
    outp = key.split('/')[-1]
    #and now create the string for the output file. this should be like any/other/subdir/prefix_
    # is speficied int he second environment variable. and then it will add output#.csv to the end
    output_file = str(os.environ['OUTPUT_FILE_PRE']) + str(outp)
    #output_file = 'subfolder/subfolder/prefix_'+str(outp)
    #simplest case is just output_file = 'prefix_'+str(outp)
    s3_resource.Object(target_bucket, output_file).put(Body=csv_buffer.getvalue())
