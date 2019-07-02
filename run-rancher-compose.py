import datetime
import json
import requests
import subprocess
import sys
import time

from credentials import *

# create submission json manually as simply the list of parameter files
# we want to run.

# read in submission json
def submit_run():
    submission = {"parameter_list":[{"Key":"parameterOptions_Standard_1600.csv"},{"Key":"parameterOptions_Standard_1700.csv"},{"Key":"parameterOptions_Standard_1800.csv"}]}
    #f = json.dumps(submission_file)
    #submission = json.load(f)

    PARAMETER_LIST = submission['parameter_list']
    TOTAL_JOBS = len(PARAMETER_LIST)

    # get yaml template
    with open(template_file, 'r') as f:
        #data = yaml.load(f)
        yaml_template = f.read()

    start = datetime.datetime.utcnow()
    for i in range(0, len(PARAMETER_LIST)):
        START_TIME = datetime.datetime.utcnow()
        PARAMETER_FILE = PARAMETER_LIST[i]['Key']
        OUTPUT_FILE = "modelRun"+str(i)

        # update yaml
        data = yaml_template.format(PARAMETER_FILE = PARAMETER_FILE,
                                    OUTPUT_FILE = OUTPUT_FILE)

        # rewrite yaml
        with open('/usr/local/sbin/docker-compose-job-submitter-{}.yml'.format(i), 'w') as f:
            f.write(data)

        # set args and call from within python
        args = ['/usr/local/sbin/rancher-compose',
                '--project-name',
                OUTPUT_FILE,
                '--verbose',
                '--file',
                '/usr/local/sbin/docker-compose-job-submitter-{}.yml'.format(i),
                '--url',
                RANCHER_URL,
                '--access-key',
                RANCHER_ACCESS_KEY,
                '--secret-key',
                RANCHER_SECRET_KEY,
                'up',
                '-d']

        print('Submitting job {} of {}'.format(i+1, len(PARAMETER_LIST)))
        subprocess.run(args = args)
    end = datetime.datetime.utcnow()
    total = (end - start).total_seconds() / 60.0

if __name__ == '__main__':
    template_file = sys.argv[1]
    submit_run()
