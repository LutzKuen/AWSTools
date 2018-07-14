import boto3
import time
import os
import configparser


class controller(object):
 def __init__(self, config_name):
  config = configparser.ConfigParser()
  conf.read(config_name)
  self.image_id = conf('AWS','image_id')
  self.type = conf('AWS','type')
  self.ec2 = boto3.resource('ec2')
  self.instance = None
  self.keyname = conf('AWS','keyname')
  self.pemfile = conf('AWS','pemfile')
  self.security_group = conf('AWS','security_group')
 def createInstance(self):
  if self.instance:
   return self.instance
  else:
   instArr = self.ec2.create_instances(
    ImageId=self.image_id,
    MinCount=1,
    MaxCount=1,
    InstanceType=self.type,
    KeyName = self.keyname,
    SecurityGroups = [self.security_group])
   self.instance = instArr[0]
   print(self.instance.id)
   self.waitUntilRunning()
   return self.instance
 def terminateInstance(self):
  if not self.instance:
   print('No running instance')
  else:
   response = self.instance.terminate()
   print(response)
 def waitUntilRunning(self):
  time.sleep(60) # TODO: try to come up with something useful
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
