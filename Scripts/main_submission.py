import os
import sys
import set_configurations as configs
import single_run
import command as cmd
import manage_dir as mdir

def Sequence(params, run_job):

  con = configs.SetConfigurations()

  i_bin_start = params['start']
  i_bin_end = min(params['end'], con.IbinMax())
  run_num = con.RunNumbers()

  n_run_total = 0
  print( '##################')
  for i_tag, tag in enumerate(con.Tags()):
    n_run_tag = 0
    print(i_tag, ': ', tag)
    con.SetOutdirname(i_tag)
    output_dirname = con.OutputDirname()
    mdir.DeleteEmptyFiles(output_dirname)
    print( '##################')
    for i_bin in range(i_bin_start, i_bin_end):
      for run in range(run_num[0],run_num[1]):
        submitted = run_job(i_bin,run,i_tag)
        n_run_total = n_run_total + submitted
        n_run_tag = n_run_tag + submitted
    print( '##################')
    if con.Notification() and (not n_run_tag == 0):
      Observation()
      n_run_total = n_run_total + 1
    print( '##################')
  return n_run_total





def Observation():
  con = configs.SetConfigurations()
  
  merge_command = None
  if con.Merge():
    merge_command = cmd.MergeCommand('no_que')
  print('merge: ', merge_command)
  
  command = cmd.CheckUpdateCommand(merge_command)
  run_command = cmd.RunCommand(command)
  master_command = cmd.MasterCommand(run_command)

  log = con.ObsLogFilename()
  err = con.ObsErrorFilename()    
  job = con.ObsJobname()    

  qsub_command = cmd.QsubCommand(master_command, job, log, err, ' --time=200:00:00 -N 1 -n 1 --mem=64G ')    
  print('Submission, Que:', con.Que())
  print(qsub_command)
  print('-')

  if con.Que() == 'test':
    print('test mode.')
  else:
    os.system(qsub_command)

def Init(params):
  con = configs.SetConfigurations()
  if params['que'] == 'test':
    yaml_file = '../Config/test.yaml'
  else:
    yaml_file = params['yaml']
  con.InitConfigs(os.getcwd(), yaml_file, params)

def Main(params):
  Init(params)
  n_run_total = Sequence(params, single_run.Run)

  print( 'Submission Ends.')
  print( 'Total: ', str(n_run_total)+'-jobs were submitted.')  
  print( '##################')

def GetParams(argc,argvs):
  print(argvs)
  print(argc)  

  if argc < 2:
    print('Please Input Options')
    print('\t$python main_submission.py PbPb (or AuAu. etc.) [eCM] [centrality (e.g. 0-5)] [alphaS] [Qs] [take_recoil 0 or 1] [PythiaGun/PGun] [bin_start] [bin_end] [quename] [yaml (optional, default: ../Config/config.yaml)]')
    print('Please Input Options')
    print('\t$python main_submission.py PP [eCM] [PythiaGun/PGun] [bin_start] [bin_end] [quename] [yaml (optional, default: ../Config/config.yaml)]')
    exit()
  
  if argvs[1] == 'PP' and argc < 7:
    print('Please Input Options')
    print('\t$python main_submission.py PP [eCM] [PythiaGun/PGun] [bin_start] [bin_end] [quename] [yaml (optional, default: ../Config/config.yaml)]')
    exit()

  if argvs[1] != 'PP' and argc < 11:
    print('Please Input Options')
    print('\t$python main_submission.py PbPb (or AuAu. etc.) [eCM] [centrality (e.g. 0-5)] [alphaS] [Qs] [take_recoil 0 or 1] [PythiaGun/PGun] [bin_start] [bin_end] [quename] [yaml (optional, default: ../Config/config.yaml)]')
    exit()

  print( '##################')
  print( '##################')
  print( 'system:', argvs[1] )
  print( 'eCM:', argvs[2] )   
  sys = argvs[1]
  ecm = int(argvs[2])

  cent = ''
  a_s = '0'
  q_s = '0'
  recoil = 0
  hard = ''
  i_bin_start = 0
  i_bin_end = 0
  que = 'primary'

  print( '------------------')
  if argvs[1] != 'PP':
    print( 'centrality:', argvs[3] )
    print( 'alphaS:', argvs[4] )
    print( 'Qs:', argvs[5] )
    no_yes = ['No','Yes']
    print( 'take recoil:', no_yes[int(argvs[6])] )
    print( '------------------')
    cent = argvs[3]
    a_s = argvs[4]
    q_s = argvs[5]
    recoil = int(argvs[6])
    ########################
    hard = argvs[7]
    i_bin_start = int(argvs[8])
    i_bin_end = int(argvs[9])
    que = argvs[10]
    #yaml_file
    if argc > 11:
      yaml_file = argvs[11]
    else:
      yaml_file = '../Config/config.yaml'
  #PP
  else: 
    hard = argvs[3]
    i_bin_start = int(argvs[4])
    i_bin_end = int(argvs[5])
    que = argvs[6]
    #yaml_file
    if argc > 7:
      yaml_file = argvs[7]
    else:
      yaml_file = '../Config/config.yaml'

  print( '------------------')
  print( 'Hard Process:', hard)
  print( 'bin:', i_bin_start, '-', i_bin_end)
  print( 'que:', que)
  print( 'yaml:', yaml_file)


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
    'end': i_bin_end,
    'que': que,
    'yaml': yaml_file
  }
  #print(params)
  return params

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = GetParams(argc, argvs)
  Main(params)
