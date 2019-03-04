# ParamUpdater

## Overview

**NOTE**: ParamUpdater requires Python version 3.6 or greater.

`ParamUpdater` is a small module that provides a programmatic way to update a parameter file.

## Setup and Usage

First, make sure the file ParamUpdater.py is in your current directory. Load
the module by running the line `from ParamUpdater import ParamUpdater` from
your Python console or script.

If you will be saving directly to S3, the `mypysql` and `boto3` libraries are
needed. Run:
  * `conda install -c anaconda pymysql boto3` if using anaconda
  * `pip install pymysql boto3` if using base python distribution

Initialize a `ParamUpdater` object by providing the filepath to the raw
parameter csv file and an optional credentials dictionary if saving to S3.
Upon initialization the `ParamUpdater` object has an
attribute `data` which contains the parameters, cleaned and parsed into a
dictionary.

The `ParamUpdater` object has the following methods available to use:

  * `ParamUpdater.get_value(param, index)` will return the value of
  a given parameter.
    - `param` - parameter to be updated
    - `index` - for Simple Tax Models this is always 0

  * `ParamUpdater.update(param, value)`
  will change a parameter to the given value.
    - `param` - parameter to be updated
    - `value` - new value for parameter

  * `ParamUpdater.write_modified(filename)` will save the modified parameters
  to a new csv file locally.
    - `filepath` - path to save the modified parameter file

  * `ParamUpdater.save_modified(filestub)` will save the modified parameter
  file to `ParamUpdater.modified_data`

_NOTE JAK-Need to check on this section_
  * `ParamUpdater.upload_modified()` will write the parameter file updates
  to the database and save the modified parameters directly to S3 in parallel.
    - `filepath` - path stub to save the modififed parameter files

  Note that this functionality requires proper AWS credentials.
  See the `configure` function in [tpc-cli](https://github.com/UI-Research/tpc-cli).
  When saving to S3, parameter changes are sent to a database, which requires
  that the `credentials` argument is properly set upon initialization. Contact
  Research Programming if you require assistance.

  * `ParamUpdater.reset()` will reset the `ParamUpdater` object to the original
  raw parameter file that was used to create the object.

Additional documentation can be found via:

```python
help(ParamUpdater)
```

from your python console after the module has been imported.

## Example Usage

A very simple use case may look like:

```python
from ParamUpdater import ParamUpdater # load module

params = ParamUpdater('parameterOptions.csv') # create parameter object from an existing file
params.update('EXEMPT', 100) # update scalar parameter
params.update('FAKE_PARAM', 'FakeData') # returns error
params.write_modified('parameterOptions_mod') # write changes to file
```

If you are writing directly to S3, make sure your `credentials` are set.
`credentials` is a dictionary of the form:

```python
credentials = {
    'host' : '[HOSTNAME HERE]',
    'port' : [PORT HERE],
    'dbname' : '[DB NAME HERE]',
    'user' : '[USERNAME HERE]',
    'password' : '[DB PASSWORD HERE]',
    }
```

The rest of the workflow would then look like:

```python
from ParamUpdater import ParamUpdater
params = ParamUpdater('parameterOptions.csv', credentials)
params.update('EXEMPT', 100) # update scalar parameter
params.save_modified('parameterOptions_mod')
params.upload_modified()
```
