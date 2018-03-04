## For Yaml Parsing purpose
#!/usr/bin/python

import os
import sys
import yaml
import json


class Utils(object):
    @classmethod
    def get_error(cls, errorlog=None):
        if errorlog:
            print ''
            print errorlog
            print 'Exiting Form Program Execution.'
            print ''
            sys.exit()

    @staticmethod
    def parse_yaml(ymlfile):
        with open(ymlfile, 'r') as yml:
            doc = yaml.load(yml)
        return doc

