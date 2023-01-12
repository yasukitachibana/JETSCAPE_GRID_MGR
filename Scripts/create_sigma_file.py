import os
import sys
import shutil
import math
import numpy as np

import numpy as np
import subprocess

def Main(argc,argvs, merge=True):

  mergedfile = ''
  readfile_template = argvs[1]
  writefile_template = argvs[2]

  i_start = 0
  i_end = 1

  if argc >= 5:
    i_start = int(argvs[3])
    i_end = int(argvs[4])
  else:
    merge=False

  if argc >= 6 and merge:
    mergedfile = argvs[5]
  #---------------------------------------
  print('-')  

  avr_val_sigma_gen = 0.0
  avr_val_sigma_err = 0.0
  num = 0  

  for i in range(i_start,i_end):
    readfile = readfile_template
    writefile = writefile_template    
    if '{}' in readfile_template:
      readfile = readfile_template.format(i)
      writefile = writefile_template.format(i)
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
    avr_val_sigma_gen = avr_val_sigma_gen + float(val_sigma_gen)
    avr_val_sigma_err = avr_val_sigma_err + float(val_sigma_err) * float(val_sigma_err)
    num = num + 1
    print('generating: '+writefile)
    simga_out_file = open(writefile,'w')  
    simga_out_file.write(data)
    simga_out_file.close

  print('-')  

  if merge:
    avr_val_sigma_gen = avr_val_sigma_gen/num
    avr_val_sigma_err = math.sqrt(avr_val_sigma_err)/num
    print('## ----------------------------------------------')               
    print('## averaged sigma = ' , avr_val_sigma_gen,' +/- ',avr_val_sigma_err)              
    print('## ----------------------------------------------')                 
    sigma_avr = np.array([avr_val_sigma_gen, avr_val_sigma_err]).T
    np.savetxt(mergedfile, [sigma_avr])

  #---------------------------------------  

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  Main(argc,argvs)

