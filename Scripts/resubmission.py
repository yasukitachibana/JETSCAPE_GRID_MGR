import os
import sys
import set_configurations as configs
import main_submission as main_sub
import shutil
import single_run

class Base:
    
  __mode = ''
  __core_function = None
  __function = None

  def __init__(self, mode):
    self.__mode = mode
    self.SetFunction()

  def SetFunction(self):
    if self.__mode == 'test':
      self.__core_function = self.PrintMode
      self.__function = self.PrintMode
    elif self.__mode == 'check and run':
      self.__core_function = single_run.Run
      self.__function = self.Function
    elif self.__mode == 'merge and transfer':
      self.__core_function = self.PrintMode
      self.__function = self.Function


  def GetFunction(self):
    return self.__function

  def PrintMode(self,i_bin,run,i_tag):
    print(self.__mode, i_bin,run,i_tag)
    return 0

  def Function(self,i_bin,run,i_tag):

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
      submitted = self.__core_function(i_bin,run,i_tag)
      print('##################################') 
      return submitted             
    else:
      print('--> Found. Skip.')
      return 0    


def Main(params):
  #base = Base('check and run')
  base = Base('merge and transfer')  
  function = base.GetFunction()
  main_sub.Sequence(params, function)

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = main_sub.GetParams(argc, argvs)
  Main(params)
