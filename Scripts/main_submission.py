import sys
import yaml
import set_configurations as configs


def Main(argc,argvs):
  print('Main')
  con = configs.SetConfigurations()
  con.InitConfigs('../Config/config.yaml')

  i_bin_start = int(argvs[-3])
  i_bin_end = min(int(argvs[-2]), con.GetIbinMax())
  print(i_bin_start,i_bin_end)

  for i_bin in range(i_bin_start, i_bin_end):
    exit()

    # code_path = gcom_gf_spath.GetCodePath()
    # print('Code Path:', code_path)
    # eCM = int(argvs[1])
    # pthat_bins = gpt.GetPtHatBins( eCM )
    
    # for BinIndex in range(int(argvs[7]),int(argvs[8])):
    #     #    for this_bin in pthat_bins:
    #     this_bin = pthat_bins[BinIndex]
    #     print('pthat_bin: ', end='')
    #     print(this_bin, end=' (GeV)\n')
    #     #if this_bin[0] >= 2:
    #     run_total = 1
    #     for run in range(0,run_total):
    #         setup.Submit(argc,argvs,code_path,this_bin,run)


def CheckArg(argc,argvs):
  print(argvs)
  print(argc)  

  if argc < 2:
    print('Please Input Options')
    print('\t$python main_submission.py AA [eCM] [centrality (e.g. 0-5)] [alphaS] [Qs] [take_recoil 0 or 1] [bin_start] [bin_end] [quename]')
    print('Please Input Options')
    print('\t$python main_submission.py PP [eCM] [centrality (e.g. 0-5)] [bin_start] [bin_end] [quename]')
    exit()
  
  if argvs[1] == 'PP' and argc < 7:
    print('Please Input Options')
    print('\t$python main_submission.py PP [eCM] [centrality (e.g. 0-5)] [bin_start] [bin_end] [quename]')
    exit()

  if argvs[1] != 'PP' and argc < 10:
    print('Please Input Options')
    print('\t$python main_submission.py AA [eCM] [centrality (e.g. 0-5)] [alphaS] [Qs] [take_recoil 0 or 1] [bin_start] [bin_end] [quename]')
    exit()

  print( '##################')
  print( '##################')
  print( 'system:', argvs[1] )
  print( 'eCM:', argvs[2] )    
  print( '------------------')
  if argvs[1] != 'PP':
    print( 'centrality:', argvs[3] )
    print( 'alphaS:', argvs[4] )
    print( 'Qs:', argvs[5] )
    no_yes = ['No','Yes']
    print( 'take recoil:', no_yes[int(argvs[6])] )
    print( '------------------')

  print( 'bin:', argvs[-3], '-', argvs[-2])
  print( 'que:', argvs[-1])  
  
  print( '##################')
  print( '##################')


if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  CheckArg(argc, argvs)
  Main(argc, argvs)
