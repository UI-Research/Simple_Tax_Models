# Simple Tax Public Models

Regardless of language, each model does the same thing.

The input file contains:
 - `itemized` - a double value with the amount of itemized deductions for the unit
 - `salary` - a double value with amount of salary for the unit.
 - `filingStatus` -  the filing status of the unit 0 indicates single and 1 indicates married.
 - `weight` - a double value with the weight of the unit.

The original datasource is the [2010 Survey of Consumer Finances](https://www.federalreserve.gov/econres/scf_2010.htm). All units with 0 salary have been removed. Input data and the SAS code used to generate the file are in the `\data` folder.

The parameters are:
  - `RATE` - a decimal value indicating the tax rate (0.1 is specified when we mean 10%)
  - `STANDARD` - a double value indicating the amount for the standard deduction
  - `EXEMPT` - a double value indicating the amount for a personal exemption.
 
The calculation for a standard deduction of $1,500 would be to choose max(itemized, 1500). At a tax rate of 10% and $1,000 of personal exemptions, the tax system is then:

```
tax = .10*[salary – max(itemized, 1500) – (1000*(1+filingStatus)]
```

The output file (`output.csv`) contains all of the input variables and adds on this tax calculation as an output to the end of the file.

The Python code in `\summarize` performs final summary tables of the output. This is run in conjunction with every version of the simulation.

The summary tables produced calculates total revenue as the sum of the calculated tax times the weight across the entire file. Then produces a table showing the sum of tax divided by salary using groupings by salary.


## C++ version
Located in the folder `\CPP`

**requirements**
- g++
- make

To build: `make all`
To run: `cppmodel.exe`
To clean: `make clean`

**notes**

Will do nothing fancy here in terms of compiling the source files in the correct order. Because we are keeping this simple, it will be easy to handle manually.

The main function is in `ModelTax.cpp` and `ModelTax.h` files. At present it, reads a couple of files: one set of data by filing unit, and one a set of options and a file `output.csv` is written out.

**Docker automated build**

To pull the image: docker pull ramanig/simple_tax_public_models:cpp-latest                                                               
To run the image: docker run ramanig/simple_tax_public_models:cpp-latest  

## Fortran version
Located in the folder `\Fortran`

**requirements**
- gfortran compiler
- make

**notes**

To build: `make`
To run: `fortmodel.exe`

**Docker automated build**

To pull the image: docker pull ramanig/simple_tax_public_models:fortran-latest                                                          
To run the image: docker run ramanig/simple_tax_public_models:fortran-latest  

## Python version
Located in the folder `\Python`
**requirements**
- Python 3

**notes**

To run: `python ModelTax.py`

**Docker automated build**

To pull the image: docker pull ramanig/simple_tax_public_models:python-latest                                                          
To run the image: docker run ramanig/simple_tax_public_models:python-latest  

# Files in the main folder
# Dockerfiles
Default Dockerfile is Fortran version, other Dockerfiles have been provided and are named using the model language they support. For example, the C++ version is named `Dockerfile_CPP`.

# Shell Scripts
Shell scripts are used to execute the models inside containers. Each is named using the model language they support. For example, the Fortran versions are named ending in `_fortran`.
