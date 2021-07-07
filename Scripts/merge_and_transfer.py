import os
import sys
import set_configurations as configs
import main_submission as main_sub
import shutil
import single_run

class Base:
    
  __mode = ''

  def __init__(self, mode):
    self.__mode = mode

  def PrintMode(self):
    print(self.__mode)

    #     self.egg = egg
    # def output(self):
    #     sum = self.ham + self.egg
    #     print("{0}".format(sum))

def CheckRun(i_bin,run,i_tag):
  con = configs.SetConfigurations()
  hadron = con.HadronListname(i_bin,run)
  parton = con.HadronListname(i_bin,run)  
  print('Check Existence of', hadron, 'and', parton)
  if (not os.path.isfile(hadron)) or (not os.path.isfile(parton)):
    print('--> Not Found. Rerun.')
    build_dir = con.BuildDirname(i_bin,run)
    if os.path.isdir(build_dir):
      print('*Delete' , build_dir)
      shutil.rmtree(build_dir)
    print('##################################')        
    submitted = single_run.Run(i_bin,run,i_tag)
    print('##################################') 
    return submitted             

  else:
    print('--> Found. Skip.')
    return 0

def Main(params):
  base = Base('test')
  base.PrintMode()
#  main_sub.Sequence(params, CheckRun)

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = main_sub.GetParams(argc, argvs)
  Main(params)
