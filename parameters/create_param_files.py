#python3
'''
@author: jkelly
'''

import sys
from ParamUpdater import ParamUpdater # load module
# when saving to AWS, keep credentials in a separate class, see README.md
# in this folder for details
#from credentials import credentials

###############
# EXAMPLE 1: making changes to a single parameter
###############
params = ParamUpdater('parameterOptions.csv')
params.update('EXEMPT', 100)
params.update('RATE',0.9)
params.update('STANDARD',2000)
#params.update('FAKE_PARAM', 'FakeData') # returns error
params.write_modified('parameterOptions_mod') # write changes to file

###############
# EXAMPLE 2: looping and incrementing
##############
params.reset()
# increment standard deduction by 100
for i in range(params.get_value('STANDARD',0)+100,2000,100):
    params.update('STANDARD',i)
    filename = 'parameterOptions_Standard_' + str(i)
    params.write_modified(filename)

# to save this batch of files to S3
#params.save_modified('parameterOptions_changeStandard')

#############
# EXAMPLE 3: Two options depend on each other
#############
params.reset()
s_inc = 50 # increment for standard deduction
e_inc = 100 # increment for exemption
# incremenent standard deduction by 50, and when it is evenly divisible by 100, increment the exmption by 100
for s in range(params.get_value('STANDARD',0)+s_inc,2000,s_inc):
    params.update('STANDARD', s)
    e = params.get_value('EXEMPT',0) #here so avail for filename
    if s%100 == 0:
        e += e_inc
        params.update('EXEMPT',e)
    filename = 'parameterOptions_Standard_' + str(s) + '_Exempt_'+ str(e)
    params.write_modified(filename)
