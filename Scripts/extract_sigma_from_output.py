import set_configurations as configs
import os
import command as cmd

def ExtractSigma(i_bin,run,i_tag):

  con = configs.SetConfigurations()
  print('Extraction of Sigma for Run '+str(run))
  output = con.OutputFilename(i_bin,run)
  print('Check Existence of', output)
  if (not os.path.isfile(output)):
    print('Error: ', output, ' has not been found. Exit.')
    exit()
  ##################
  sigmafile = ''
  ##################
  command = cmd.ExtractSigmaCommand(output,sigmafile)
  
  # run_command = cmd.RunCommand(command)
  # master_command = cmd.MasterCommand(run_command)
  # ##################
  # if con.Que() == 'test':
  #   print('test mode')
  #   print('Submission, Main Command')
  #   print(master_command)
  #   print('-')
  #   os.system(master_command)
  #   #exit()
  # else:
  #   log = con.LogFilename(i_bin,run)
  #   err = con.ErrorFilename(i_bin,run)    
  #   job = con.Jobname(i_bin,run)    
  #   qsub_command = cmd.QsubCommand(master_command, job, log, err)    
  #   print('Submission, Que:', con.Que())
  #   print(qsub_command)
  #   print('-')
  #   os.system(qsub_command)

  return 1