import os
import sys
import shutil

import numpy as np
import subprocess

def Main(argc,argvs):

  readfile = argvs[1]
  writefile = argvs[2]

  #---------------------------------------
  print('-')  

  print('Read File: ', readfile)  
  with open(readfile, mode='r') as f:
    lines = f.readlines()

  lines = [line.strip() for line in lines]
  l_sigma_gen = [line for line in lines if 'sigmaGen' in line]
  l_sigma_err = [line for line in lines if 'sigmaErr' in line]
        
  val_sigma_gen = l_sigma_gen[-1].split()[-1]
  val_sigma_err = l_sigma_err[-1].split()[-1]    

  print('## ----------------------------------------------')               
  print('## sigma = ' , val_sigma_gen,' +/- ',val_sigma_err)              
  print('## ----------------------------------------------')                 
  #---------------------------------------
  #---------------------------------------  
  data = val_sigma_gen +' '+val_sigma_err+'\n'
  print('generating: '+writefile)
  simga_out_file = open(writefile,'w')  
  simga_out_file.write(data)
  simga_out_file.close

  print('-')  
  #---------------------------------------  

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  Main(argc,argvs)

