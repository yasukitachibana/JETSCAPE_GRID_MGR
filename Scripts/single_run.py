import set_configurations as configs
import sys
import os
import shutil
import set_xml
import manage_dir as mdir
import command as cmd

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

def GetParams(argc,argvs):
  print(argvs)
  print(argc)  

  if argc < 2:
    print('Please Input Options')
    print('\t$python main_submission.py AA [eCM] [centrality (e.g. 0-5)] [alphaS] [Qs] [take_recoil 0 or 1] [PythiaGun/PGun] [bin_start] [quename]')
    print('Please Input Options')
    print('\t$python main_submission.py PP [eCM] [centrality (e.g. 0-5)] [PythiaGun/PGun] [bin_start] [quename]')
    exit()
  
  if argvs[1] == 'PP' and argc < 7:
    print('Please Input Options')
    print('\t$python main_submission.py PP [eCM] [centrality (e.g. 0-5)] [PythiaGun/PGun] [bin_start] [quename]')
    exit()

  if argvs[1] != 'PP' and argc < 10:
    print('Please Input Options')
    print('\t$python main_submission.py AA [eCM] [centrality (e.g. 0-5)] [alphaS] [Qs] [take_recoil 0 or 1] [PythiaGun/PGun] [bin_start] [quename]')
    exit()

  print( '##################')
  print( '##################')
  print( 'system:', argvs[1] )
  print( 'eCM:', argvs[2] )   
  sys = argvs[1]
  ecm = int(argvs[2])

  cent = ''
  a_s = 0.0
  q_s = 0.0
  recoil = 0
  print( '------------------')
  if argvs[1] != 'PP':
    print( 'centrality:', argvs[3] )
    print( 'alphaS:', argvs[4] )
    print( 'Qs:', argvs[5] )
    no_yes = ['No','Yes']
    print( 'take recoil:', no_yes[int(argvs[6])] )
    print( '------------------')
    cent = argvs[3]
    a_s = float(argvs[4])
    q_s = float(argvs[5])
    recoil = int(argvs[6])

  print( 'Hard Process:', argvs[-3])
  print( 'bin:', argvs[-2])
  print( 'que:', argvs[-1])  
  
  hard = argvs[-3]
  i_bin_start = int(argvs[-2])
  que = argvs[-1]
  print( '##################')
  print( '##################')

  params = {
    'system': sys,
    'eCM': ecm,
    'centrality': cent,
    'alphas': a_s,
    'Qsw': q_s,
    'recoil': recoil,
    'hard': hard,
    'start': i_bin_start,
    'end': i_bin_start+1,
    'que': que
  }
  #print(params)
  return params

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = GetParams(argc, argvs)
  con = configs.SetConfigurations()
  con.InitConfigs(os.getcwd(), '../Config/config.yaml', params)
  Run(params['start'],0)



