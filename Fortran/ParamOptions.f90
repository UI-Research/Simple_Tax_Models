!
!Parameter options file read and save
!

module ParamOptions
use declarations

implicit none
save

contains

! Description: Reads the parameterOptions.csv file
!
! Remarks: Assume that the order that these are given is constant. fortran doesn't like anything
! too clever. Could use JSON as the input format instead if wanted to be more flexible. Keeping
! that complexity out of this version, because it requires external libraries.
! or maybe not?
! https://jblevins.org/log/control-file
subroutine readParams
  character*128 dummychar
  open(unit=parameterfile, file=file11, status='old', action='read')
    read(parameterfile,*), dummychar, rate
    read(parameterfile,*), dummychar, standard
    read(parameterfile,*), dummychar, exempt
    !print *, "checking value read ", rate, standard, exempt
  close(parameterfile)
end subroutine


end module
