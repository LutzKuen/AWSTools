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


import boto3
import time
import os
from configparser import ConfigParser


class controller(object):
 def __init__(self, config_name):
  conf = ConfigParser()
  conf.read(config_name)
  self.image_id = conf.get('AWS','image_id')
  self.type = conf.get('AWS','type')
  self.ec2 = boto3.resource('ec2')
  self.instance = None
  self.maxprice = conf.get('AWS','max_price')
  self.keyname = conf.get('AWS','keyname')
  self.pemfile = conf.get('AWS','pemfile')
  self.security_group = conf.get('AWS','security_group')
 def createInstance(self):
  marketOptions = { 'MarketType': 'spot', 'SpotOptions': { 'MaxPrice': self.maxprice }}
  if self.instance:
   return self.instance
  else:
   instArr = self.ec2.create_instances(
    ImageId=self.image_id,
    MinCount=1,
    MaxCount=1,
    InstanceType=self.type,
    KeyName = self.keyname,
    InstanceMarketOptions = marketOptions,
    SecurityGroups = [self.security_group])
   self.instance = instArr[0]
   print(self.instance.id)
   #self.waitUntilRunning()
   return self.instance
 def terminateInstance(self):
  if not self.instance:
   prent('No running instance')
  else:
   response = self.instance.terminate()
   print(response)
 def waitUntilRunning(self):
  while True:
   client = boto3.client('ec2')
   response = client.describe_instances(InstanceIds = [self.instance.instance_id])
   state = response['Reservations'][0]['Instances'][0]['State']['Code']
   if state == 16:
    return
   else:
    print('Instance ' + str(instance.id) + ', state: ' + str(state))
    time.sleep(10)
 def transferFilesToWorker(self, filesList):
  if not self.instance:
   print('Instantiate a worker first')
   return
  client = boto3.client('ec2')
  response = client.describe_instances(InstanceIds = [self.instance.instance_id])
  self.public_dns = response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicDnsName'] # this is weird, but this is how it is
  for _file in filesList:
   scpstr = 'scp -o StrictHostKeyChecking=no -i ' + self.pemfile + ' '  + _file + ' ubuntu@' + self.public_dns + ':~/'
   print(scpstr)
   os.system(scpstr)
 def execOnRemote(self, scriptName):
  if not self.public_dns:
   print('unable to execute: NO remote public dns')
  sshString = 'ssh -o StrictHostKeyChecking=no -i ' + self.pemfile + ' ubuntu@' + str(self.public_dns) + " 'bash -s' < " + scriptName
  print(sshString)
  os.system(sshString)
 def retrieveResults(self, resultsNames):
  if not self.instance:
   print('Instantiate a worker first')
   return
  for _file in resultsNames:
   scpstr = 'scp -i ' + self.pemfile + ' ubuntu@' + self.public_dns + ':' + _file + ' .'
   print(scpstr)
   os.system(scpstr)
