import os
import sys
import set_configurations as configs
import single_run


def Main(params):
  print('Main')
  con = configs.SetConfigurations()
  con.InitConfigs(os.getcwd(), '../Config/config.yaml', params)

  i_bin_start = params['start']
  i_bin_end = min(params['end'], con.IbinMax())

  for i_bin in range(i_bin_start, i_bin_end):
    run_total = con.RunTotal()
    for run in range(0,run_total):
      single_run.Run(i_bin,run)


def GetParams(argc,argvs):
  print(argvs)
  print(argc)  

  if argc < 2:
    print('Please Input Options')
    print('\t$python main_submission.py AA [eCM] [centrality (e.g. 0-5)] [alphaS] [Qs] [take_recoil 0 or 1] [PythiaGun/PGun] [bin_start] [bin_end] [quename]')
    print('Please Input Options')
    print('\t$python main_submission.py PP [eCM] [centrality (e.g. 0-5)] [PythiaGun/PGun] [bin_start] [bin_end] [quename]')
    exit()
  
  if argvs[1] == 'PP' and argc < 8:
    print('Please Input Options')
    print('\t$python main_submission.py PP [eCM] [centrality (e.g. 0-5)] [PythiaGun/PGun] [bin_start] [bin_end] [quename]')
    exit()

  if argvs[1] != 'PP' and argc < 11:
    print('Please Input Options')
    print('\t$python main_submission.py AA [eCM] [centrality (e.g. 0-5)] [alphaS] [Qs] [take_recoil 0 or 1] [PythiaGun/PGun] [bin_start] [bin_end] [quename]')
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

  print( 'Hard Process:', argvs[-4])
  print( 'bin:', argvs[-3], '-', argvs[-2])
  print( 'que:', argvs[-1])  
  
  hard = argvs[-4]
  i_bin_start = int(argvs[-3])
  i_bin_end = int(argvs[-2])
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
    'end': i_bin_end,
    'que': que
  }
  #print(params)
  return params

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = GetParams(argc, argvs)
  Main(params)