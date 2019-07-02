# Simple_Tax_Public_Model
# Fortran version, practice commit to test docker autobuild

# start by building the basic container
FROM centos:latest
MAINTAINER Jessica Kelly <jkelly@urban.org>
RUN yum update -y
# add fortran
RUN yum install -y gcc-gfortran gdb make
# and python and related requirements
RUN yum -y install epel-release && yum clean all
RUN yum -y install python-pip && yum clean all
#add aws cli
RUN pip install awscli
ENV REGION=us-east-1

# build the model code - note the copy from the parent directory of the bash script and requirements
COPY Fortran/Makefile run_fortran.sh requirements.txt Fortran/*.f90 Fortran/parameterOptions.csv /Fortran/
COPY data/Demo.csv /data/


# set working directory to Fortran and then build the model
WORKDIR /Fortran/
#add python requirements
RUN pip install -r requirements.txt
RUN make

# configure the container to run the executable by default
# CMD ["./fortmodel"] #this is simplest way to run the exe, but need more steps so use bash
ENTRYPOINT ["/Fortran/run_fortran.sh"]
