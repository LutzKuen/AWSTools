#!/usr/bin/env python
__author__ = "Lutz Künneke"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lutz Künneke"
__email__ = "lutz.kuenneke89@gmail.com"
__status__ = "Prototype"
"""
Simple wrapper for the boto3 API which makes it easier if 
you need just one worker instance which has to carry out 
a specific task and then should be terminated after retrieving 
the result files
Author: Lutz Kuenneke, 12.07.2018
"""

import os
import time
from configparser import ConfigParser

import boto3


class Controller(object):
    def __init__(self): #, config_name):
        #conf = ConfigParser()
        #conf.read(config_name)
        #self.image_id = conf.get('AWS', 'image_id')
        #self.type = conf.get('AWS', 'type')
        self.ec2 = boto3.resource('ec2')
        #self.instance = None
        #self.keyname = conf.get('AWS', 'keyname')
        #self.pemfile = conf.get('AWS', 'pemfile')
        #self.security_group = conf.get('AWS', 'security_group')

    def get_own_credits(self):
        #client = boto3.client('ec2')
        instances = self.ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            print(instance.id, instance.instance_type)
