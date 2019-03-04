libname in 'D:\SCF10';

data temp; set in.p10i6;
	keep IDN Schedule_A Salary Filing_stat wgt;

	if x5744=2 then delete;
	if x5746 in (2,4,5) then delete;
	IDN=y1;

	Schedule_A=x5823;
	Salary=x4112+x4712;
	if salary=0 then delete;
	
	Filing_stat=(x5746=1);

	wgt=x42001/5;
run;

proc univariate;
var schedule_a;
weight wgt;
where schedule_a>0;
run;


PROC EXPORT DATA= WORK.TEMP 
            OUTFILE= "D:\Demo.csv" 
            DBMS=CSV REPLACE;
     PUTNAMES=YES;
RUN;
