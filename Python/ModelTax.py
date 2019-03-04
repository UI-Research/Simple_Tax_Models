# -*- coding: utf-8 -*-
import csv
from io import open

filers = []
opts = []
filer = {}
#    
#def readAllFile(inputFile):
#    try:
#        with open(inputFile, newline = '') as file:
#            reader = csv.reader(file)
#            for row in reader:
#                if (row != ''):
#                    try:
#                        filers.append(TaxFiler())
#                    except Exception as ex :
#                        print('Error TaxFiler {}'.format(type(ex)))
#                    else:
#                        filers[len(filers) - 1].extractVarsFromLine(row)
#    except OSError:
#        print('Failed to Open ' + inputFile)
#    
#def testCalc():
#    findIt = 'RATES1'
#    rates = findValue(findIt)
#    if (rates == -999999):
#        rates = 1
#    for file in filers:
#        file.testOutputVariable = file.salary * rates

#def writeAllOutput(outFile):
#    with open(outFile, 'a') as f:
#        writer = csv.writer(f)
#        for file in filers:
#            writer.writerow(file)

#calculates tax in very simple manner
def calcTax(salary, itemized, standard, rate, exempt, filingStatus):
    tax = rate * (salary - max(itemized, standard) - (1000 * (1 + filingStatus)))
    return tax
 
#testOutputVariable renamed tax
def filerExtractVarsFromLine(inputList):
    taxfiler = {'unitId': inputList[0], 'itemized': float(inputList[1]), 'salary': float(inputList[2]), 'filingStatus':
        int(inputList[3]), 'weight': float(inputList[4]), 'tax': 0.0}
    return taxfiler

def paramExtractVarsFromLine(inputList):
    paramopts = {'label': inputList[0], 'value': float(inputList[1])}
    return paramopts


def readParams(inOpts):
    try:
        with open(inOpts, 'r', newline ='') as file:
            reader = csv.reader(file)
            for row in reader:
                if (row != ''):
                    try:
                        opts.append(paramExtractVarsFromLine(row))
                    except Exception as ex:
                        print('Error ParamOptions {}'.format(type(ex)))
    except OSError:
        print('Failed to Open ' + inOpts)
    
def findValue(label):
    retValue = 999999
    for opt in opts:
        if opt['label'] == label:
            retValue = opt['value']
    return retValue
   
#in main method in c++ version     
def writeOutput(filers, outFile):
    headers = ['unitId', 'itemized', 'salary', 'filingStatus', 'weight', 'tax']
    with open(outFile, 'w', newline = '') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for filer in filers:
            writer.writerow(filer)
        
if __name__ == '__main__':
    print('Python Based Simple Tax Public Model Example')
    inputFile = "..//data//Demo.csv"
    inOpts = "parameterOptions.csv"
    outFile = "output.csv"
    readParams(inOpts)
    count = 0
    try:
        with open(inputFile, 'r', newline = '') as file:
            reader = csv.reader(file)
            for row in reader:
                count += 1
                if (row != ''):
                    filer = filerExtractVarsFromLine(row)
                standard = findValue("STANDARD")
                if (standard == -999999):
                    standard = 1000
                rate = findValue("RATE")
                if (rate == -999999):
                    rate = 0.1
                exempt = findValue("EXEMPT")
                if (exempt == -999999):
                    exempt = 1000
                tax = calcTax(filer['salary'], filer['itemized'], standard, rate, exempt, filer['filingStatus'])
                filer['tax'] = tax
                filers.append(filer)
                if(count%10000 == 0):
                    print('{} observations processed'.format(count))
    except OSError:
        print('Failed to Open ' + inputFile)
        
    print('{} total observations processed'.format(count))
    writeOutput(filers, outFile)
    print('output file ' + outFile + ' written')
    print('processing complete!')

   