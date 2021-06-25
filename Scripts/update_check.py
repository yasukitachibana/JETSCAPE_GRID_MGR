import os
import sys
import subprocess
import glob
import time
import datetime

def UpdateCheck(dirname, email):

  while CheckTime(dirname):
    print(datetime.datetime.now(), "| Checked ", dirname)
    time.sleep(600)
  mail_text = "No Update in " + str(dirname)
  os.system('echo ' + mail_text + ' | sendmail ' + email)
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



def main():
  
  import argparse
    
  parser = argparse.ArgumentParser()
  parser.add_argument("--d", type=str, default="NONE")
  parser.add_argument("--e", type=str, default="NONE")  
  args = parser.parse_args()
    
  if args.d == "NONE":
    print( "Please specify directory name with --d [DIR_NAME]" )
    exit()
  if args.e == "NONE":
    print( "Please specify email with --e [EMAIL]" )
    exit()
        
  UpdateCheck(args.d,args.e)
  
if __name__ == '__main__':
  main()
