#python3

"""
Kyle Ueyama
Jessica Kelly
Urban Institute
Python 3.6.1
"""
import boto3
import json
import os.path
import re

class ParamUpdater:
    """
    Programatically update a Simple Tax Model parameter file.

    ParamUpdater will create an object containing parsed parameter data
    from the original csv file. From there, four methods can be called:
        * update - change the value of a parameter
        * get_value - obtain the value of a parameter
        * write_modified - write modified file to csv
        * save_modified - save modified file to AWS S3
        * reset - reset to original parameter file

    Args:
        raw_filepath (str): Full filepath to the original parameter file
        credentials (dict): Optional dictionary of database credentials (when saving to AWS S3)

    Attributes:
        data (dict): Parameter data parsed from original csv file
        updates (dict): Log of parameters that have been changed and new values
    """

    def __init__(self, raw_filepath, credentials=None):
        self.raw_filepath = raw_filepath
        self.credentials = credentials
        self.counter = 0
        self.data = {}
        self.updates = {}
        self._convert_raw(raw_filepath)

    def _convert_raw(self, raw_filepath):
        """
        Parse the original csv parameter file to dict for update.

        Args:
            raw_filepath (str): Full filepath to the original parameter file.

        Attributes:
            data (dict): Parameter data parsed from original csv file.
        """
        if os.path.splitext(raw_filepath)[1] == '':
            raw_filepath += '.csv'
        with open(raw_filepath, 'r') as csvfile:
            for row in csvfile:
                row = row.replace('\n', '').split(',')
                header = row.pop(0).replace(':', '').strip()
                self.data[header] = [item for item in row if item not in '']
        for key in self.data.keys():
            index = 0
            for value in self.data[key]:
                if re.search('\.[A-Z]*\.', value):
                    self.data[key][index] = json.loads(value.lower().replace('.', ''))
                elif re.search('[0-9]*[A-Z]*\.[0-9]+', value) or value == '0':
                    self.data[key][index] = float(value)
                elif re.search('^\d+$', value):
                    self.data[key][index] = int(value)
                else: pass
                index+=1

    def update(self, param, value):
        """
        Update a parameter to a new value.

        Args:
            param (str): Name of the parameter to be updated.
            value (varies): New value for the parameter to be set.

        Attributes:
            data (dict): Modified parameter data.
        """
        if param not in self.data.keys():
            print('Error: parameter {0} not found. No update made.'.format(param))
            return None
        # check the data type so we know what kind of update to perform
        # index is always 0 because we do not have more than one value per
        # row in the simple example
        index = 0
        if isinstance(self.data[param][index], bool):
            self._set_bool(param, value, index)
        elif isinstance(self.data[param][index], int):
            self._set_int(param, value, index)
        elif isinstance(self.data[param][index], float):
            self._set_float(param, value, index)
        elif isinstance(self.data[param][index], str):
            self._set_string(param, value, index)
        else:
            raise ValueError('Error: parameter {0} not found. No update made.'.format(param))
        #self._add_update(param, value)

    def _set_int(self, param, value, index):
        """
        Set parameters of type int.

        Args:
            param (str): Parameter to be updated.
            value (int): New value for the parameter to be set.
            index (int): Position of original parameter value to be updated.
        """
        if type(value) == int:
            self.data[param][index] = value
        elif type(value) == float:
            self.data[param][index] = value
            print('Warning: {} was read from the base file as an integer.'.format(param))
        else:
            raise ValueError('{0} must be type int. No update made.'.format(param))

    def _set_float(self, param, value, index):
        """
        Set parameters of type float.

        Args:
            param (str): Parameter to be updated.
            value (float): New value for the parameter to be set.
            index (int): Position of original parameter value to be updated.
        """
        if type(value) == float or value == 0:
            self.data[param][index] = value
        elif type(value) == int:
            self.data[param][index] = value
            print('Warning: {} was read from the base file as a float.'.format(param))
        else:
            raise ValueError('{0} must be type float. No update made.'.format(param))

    def _set_bool(self, param, value, index):
        """
        Set parameters of type bool.

        Args:
            param (str): Parameter to be updated.
            value (bool): New value for the parameter to be set.
            index (int): Position of original parameter value to be updated.
        """
        if type(value) == bool:
            self.data[param][index] = value
        else:
            raise ValueError('{0} must be type bool. No update made.'.format(param))

    def _set_string(self, param, value, index):
        """
        Set parameters of type str.

        Args:
            param (str): Parameter to be updated.
            value (str): New value for the parameter to be set.
            index (int): Position of original parameter value to be updated.
        """
        if type(value) == str:
            self.data[param][index] = value
        else:
            raise ValueError('{0} must be type str. No update made.'.format(param))

    def write_modified(self, modified_filepath):
        """
        Write the modified parameter data to csv and json.

        Args:
            modified_filepath (str): Full filepath for the modified parameter file.
        """
        #os.makedirs(os.path.dirname(modified_filepath), exist_ok = True)
        with open(modified_filepath+'.csv', 'w') as csvfile:
            for key in self.data:
                csvfile.write(key)
                #used when we need special whitespace
                #if len(key) < 22:
                #    csvfile.write(' ' * (21 - len(key)))
                #key_length = self.length - len(self.data[key])
                key_length = len(self.data[key])
                for i in range(0, len(self.data[key])):
                    if type(self.data[key][i]) == bool:
                        csvfile.write(','+'.{0}.'.format(str(self.data[key][i]).upper()))
                    elif type(self.data[key][i]) == float and self.data[key][i] == 0.0:
                        self.data[key][i] = int(self.data[key][i])
                        csvfile.write(','+str(self.data[key][i]))
                    else:
                        csvfile.write(','+str(self.data[key][i]))
                #adds a , at the end of a line
                #csvfile.write(','*key_length)
                csvfile.write('\n')
        print('Creating parameter file: {}.csv'.format(modified_filepath))

    def save_modified(self, path):
        """
        Save a modified parameter file to S3

        Args: path (str): parameter file stub name
        """
        print("Modify bucket name to proceed")
        bucket = 'your.bucket.name'
        body = ''
        for key in self.data:
            body += key
            #if len(key) < 22:
            #    body += (' ' * (21 - len(key)))
            #key_length = self.length - len(self.data[key])
            key_length = len(self.data[key])
            for i in range(0, len(self.data[key])):
                if type(self.data[key][i]) == bool:
                    #self.data[key][i] = '.{0}.'.format(str(self.data[key][i]).upper())
                    body += (','+'.{0}.'.format(str(self.data[key][i]).upper()))
                elif type(self.data[key][i]) == float and self.data[key][i] == 0.0:
                    self.data[key][i] = int(self.data[key][i])
                    body += (','+str(self.data[key][i]))
                else:
                    body += (','+str(self.data[key][i]))
            #body += (','*key_length)
            body += '\n'
        #######
        #MODIFY THE SECTION TO SUIT YOUR NEEDS
        ######
        print('Modify the code section below before running')
        #s3 = boto3.client('s3', region_name = 'us-east-1')
        #self.counter += 1
        #modified_path = 'your/path' + path + '-{}.csv'.format(self.counter)
        #s3.put_object(Bucket = bucket, Key = modified_path, Body = body)
        #self._insert_changes(modified_path.replace('your/path', ''))
        print('Saving parameter file ' + modified_path + ' to S3' )

    def get_value(self, param, index):
        """
        Return the value of a given parameter.

        Args:
            param (str): parameter to be returned
            index (int): Position of original parameter value.
        """
        try:
            return self.data[param][index]
        except:
            print('Error: parameter {0} not found.'.format(param))

    def reset(self):
        """
        Reset data to original from parameter file.
        Reset updates to empty dictionary.
        """
        self.data = {}
        self.updates = {}
        self._convert_raw(self.raw_filepath)
