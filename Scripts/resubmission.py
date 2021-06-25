import os
import sys
import set_configurations as configs
import main_submission as main_sub
import shutil
import single_run

def CheckRun(i_bin,run):
  con = configs.SetConfigurations()
  hadron = con.HadronListname(i_bin,run)
  print('Check Existence of', hadron)
  if not os.path.isfile(hadron):
      print('-->', hadron , ': Not Found. Rerun.')
      build_dir = con.BuildDirname(i_bin,run)
      if os.path.isdir(build_dir):
        print('*Delete' , build_dir)
        shutil.rmtree(build_dir)
      print('##################################')        
      single_run.Run(i_bin,run)
      print('##################################')              
  else:
    print('--> Found. Skip.')

def Main(params):
  main_sub.Sequence(params, CheckRun)

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = main_sub.GetParams(argc, argvs)
  Main(params)