import os
import sys
import set_configurations as configs
import main_submission as main_sub
import run_jetscape as rj

import command as cmd

def GenerateSigmaMain():
  print( 'Start Generating Sigma Files')
  con = configs.SetConfigurations()
  run_num = con.RunNumbers()

  i_bin_start = params['start']
  i_bin_end = min(params['end'], con.IbinMax())
  print('bin:', i_bin_start,'-',i_bin_end)

  for i_bin in range(i_bin_start, i_bin_end):
    output = con.OutputFilename(i_bin,{})
    sigmafile = con.SigmaFilename(i_bin,{})
    run_start = run_num[0]
    run_end = run_num[1]
    mergedsigmafile = con.MergedSigmaFilename(i_bin)
    print(output,sigmafile,mergedsigmafile)
    print(run_start,run_end)
    ##################
    command = cmd.ExtractSigmaCommand(output,sigmafile,run_start,run_end,mergedsigmafile)
    run_command = cmd.RunCommand(command)
    master_command = cmd.MasterCommand(run_command)
    print(command)

  ##################
  if con.Que() == 'test':
    print('test mode')
    print('Submission, Main Command')
    print(master_command)
    print('-')
    os.system(master_command)
    #exit()
  else:
    run_info = str(run_start)+'-'+str(run_end)
    log = con.LogFilename(i_bin,run_info,'Sigma')
    err = con.ErrorFilename(i_bin,run_info,'Sigma')    
    job = con.Jobname(i_bin,run_info,'Sigma')    
    qsub_command = cmd.QsubCommand(master_command, job, log, err)    
    print('Submission, Que:', con.Que())
    print(qsub_command)
    print('-')
    os.system(qsub_command)

  
  print( '##################')


#       hadron = con.HadronListname(i_bin,'*')
#       hadron_merged = con.MergedHadronListname(i_bin)      
#       parton = con.PartonListname(i_bin,'*')
#       parton_merged = con.MergedPartonListname(i_bin)      
#       Write(hadron,hadron_merged,i_bin)
#       print('------')
#       Write(parton,parton_merged,i_bin)        
#       print( '------------------')
#       os.system(chmod_cmd)
#   print( 'Finish Merging')
#   print( '##################')

def Main(params):

  main_sub.Init(params)
  
  base = rj.Base('generate cross section file(s)')  
  function = base.GetFunction()
  con = configs.SetConfigurations()
  con.NotificationOff()
  ##==========================
  n_run_total = main_sub.Sequence(params, function)
  print( 'Total: ', str(n_run_total)+'-jobs are incompleted.') 
  if n_run_total > 0:
    print( '--> Exit.') 
    #exit()
  print( '##################')
  ##==========================
  GenerateSigmaMain()


if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = main_sub.GetParams(argc, argvs)
  Main(params)
