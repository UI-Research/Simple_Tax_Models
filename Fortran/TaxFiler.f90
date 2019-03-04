module TaxFiler
use declarations

implicit none
save

contains

  ! Description: Calculates tax in a very simple manner.
  !
  ! Remarks: Everything is globally declared in declarations, so no need to pass parameters.
  subroutine calcTax
    tax = rate *(salary - max(itemized, standard) - 1000 * (1 + filingStatus));
  end subroutine


end module
