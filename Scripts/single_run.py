import set_configurations as configs
import sys
import os
import shutil
import set_xml
import manage_dir as mdir
import command as cmd
import main_submission as main_sub

def Run(i_bin,run,i_tag):

  con = configs.SetConfigurations()
  print('run '+str(run))
  ##################
  mdir.Mkdirs(con.OutputDirname())
  mdir.Mkdirs(con.LogDirname())  
  build_dir = con.BuildDirname(i_bin,run)
  if os.path.isdir(build_dir):
      print('*Delete' , build_dir)
      shutil.rmtree(build_dir)
  mdir.Mkdirs(build_dir)
  ##################
  set_xml.SetXml(i_bin, run, i_tag)
  ##################
  command = cmd.Command(i_bin,run)
  run_command = cmd.RunCommand(command)
  master_command = cmd.MasterCommand(run_command)
  ##################
  if con.Que() == 'test':
    print('test mode')
    print('Submission, Main Command')
    print(master_command)
    print('-')
    os.system(master_command)
    #exit()
  else:
    log = con.LogFilename(i_bin,run)
    err = con.ErrorFilename(i_bin,run)    
    job = con.Jobname(i_bin,run)    
    qsub_command = cmd.QsubCommand(master_command, job, log, err)    
    print('Submission, Que:', con.Que())
    print(qsub_command)
    print('-')
    os.system(qsub_command)

  return 1

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = main_sub.GetParams(argc, argvs)  
  con = configs.SetConfigurations()
  params['end'] = params['start']+1  
  con.InitConfigs(os.getcwd(), params['yaml'], params)
  Run(params['start'],0)



