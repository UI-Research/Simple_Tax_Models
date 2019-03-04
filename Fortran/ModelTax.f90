! Main  program flow.
! Make sure to be mindful of looping
!


program ModelTax
use ParamOptions
use declarations
use TaxFiler

implicit none

character*128 dummychar
integer count
integer io



write(*,*) "Fortran-based Simple Tax Public Model Example"
! read parameters, need to know up-front
! this will make sure that variables rate, standard, exempt are set (even if not in parameter file)
call readParams

! big loop here that does most of the work
! open the main input file and start to read it
open(unit=datafile, file=file12, status='old', action='read')
! open the output file so that we can write to it as we go
open(unit=outputfile, file=file20, action='write')
! write header
write(outputfile,*), "unitId,itemized,salary,filingStatus,weight,tax"
! We know there are 20017 records in the input file, but read as if we don't
count = 0
do
  read(datafile,*,IOSTAT=io) unitId, itemized, salary, filingStatus, weight
  if (io/=0) exit ! exit at the end or if some error reading happens
  count = count + 1
  !print *, "test read ", unitId, itemized, salary, filingStatus, weight
  if(mod(count,10000).eq.0) then
    write(*,*) count, " observations processed."
  end if
  ! do calculations
  call calcTax

  ! write output, brute force comma-delimited.
  write(outputfile,*)unitId,",",itemized,",",salary,",",filingStatus,",",weight,",",tax
end do
write(*,*) count, " total observations processed."






close (datafile)
close (outputfile)
end program
