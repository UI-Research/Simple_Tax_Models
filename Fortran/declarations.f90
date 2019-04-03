! use for global variables
module declarations

save

! For the parameters we will read. For simplicity, keep all as doubles.
double precision :: rate, standard, exempt

! Unit numbers for files
integer, parameter :: parameterfile = 11
integer, parameter :: datafile = 12
integer, parameter :: outputfile = 20

! paths for files
character*128 :: file11 !parameter file
character*128, parameter :: file12 = '..//data//Demo.csv'
!character*128, parameter :: file12 = 'test.csv' ! small file used for testing
character*128 :: file20 !output file

! variables from input file
character*8 unitId
double precision :: itemized, salary, filingStatus, weight

! calculated variables
double precision:: tax
end module
