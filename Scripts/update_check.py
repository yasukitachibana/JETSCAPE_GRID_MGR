import os
from posixpath import dirname
import sys
import subprocess
import glob
import time
import datetime

def UpdateCheck(dirname, email, command):

  while CheckTime(dirname):
    print(datetime.datetime.now(), "| Checked ", dirname)
    time.sleep(300)
  mail_text = "No Update in " + str(dirname)
  os.system('echo ' + mail_text + ' | sendmail ' + email)
  if not command  == None:
    os.system(command)  
  print('Sent Notification Email. Exit.')

def CheckTime(dirname):
  current_time = time.time()
  print()

  files = glob.glob(os.path.join(dirname,'*'))
  files.sort(key = os.path.getmtime)
  latest_file = files[-1]
  t = os.path.getmtime(latest_file)
  #  print(t)
  #  print(latest_file)
  
  td = current_time - t
  #print(td)

  if(td>1200):
    return False
  return True

def main(argc, argvs):
  
  if argc < 3:
    print( "Please specify directory name and email address" )
    print( "python update_check [DIR_PATH] [EMAIL]" )    
    exit()

  dirname = argvs[1]
  email = argvs[2]  

  print('dirname:' , dirname)
  print('email:' , email)  
  command = None
  if argc > 3:
    command = ' '.join(argvs[3:])
    print('command:' , command)

  UpdateCheck(dirname, email, command)
  
if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  main(argc, argvs)
