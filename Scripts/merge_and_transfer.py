import os
import sys
import set_configurations as configs
import main_submission as main_sub
import shutil
import single_run
import run_jetscape as rj
import manage_dir as mdir

def Write(input, output):
  print('merge', input)
  print('-->', output)
  command = 'cat {} > {}'.format(input,output)
  os.system(command)


def Merge():
  print( 'Start Merging')
  con = configs.SetConfigurations()

  i_bin_start = params['start']
  i_bin_end = min(params['end'], con.IbinMax())

  for i_tag, tag in enumerate(con.Tags()):
    print(i_tag, ': ', tag)
    con.SetOutdirname(i_tag)
    print(con.MergedDirname())
    mdir.Mkdirs(con.MergedDirname())
    print( '------------------')
    for i_bin in range(i_bin_start, i_bin_end):
      hadron = con.HadronListname(i_bin,'*')
      hadron_merged = con.MergedHadronListname(i_bin)      
      parton = con.PartonListname(i_bin,'*')
      parton_merged = con.MergedPartonListname(i_bin)      
      Write(hadron,hadron_merged)
      print('------')
      Write(parton,parton_merged)        
      print( '------------------')
  print( 'Finish Merging')
  print( '##################')

def Main(params):

  main_sub.Init(params)
  
  base = rj.Base('merge and transfer')  
  function = base.GetFunction()
  con = configs.SetConfigurations()
  con.NotificationOff()
  ##==========================
  n_run_total = main_sub.Sequence(params, function)
  print( 'Total: ', str(n_run_total)+'-jobs are incompleted.') 
  if n_run_total > 0:
    print( '--> Exit.') 
    exit()
  print( '##################')
  ##==========================
  Merge()


if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = main_sub.GetParams(argc, argvs)
  Main(params)
