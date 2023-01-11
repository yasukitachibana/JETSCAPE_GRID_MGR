import os
import sys
import set_configurations as configs
import main_submission as main_sub
import extract_sigma_from_output as ext_sig
import shutil
import single_run
import command as cmd

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
      self.__core_function = self.ReturnOne
      self.__function = self.Function
    elif self.__mode == 'generate cross section file(s)':
      self.__core_function = ext_sig.ExtractSigma
      self.__function = self.Function


  def GetFunction(self):
    return self.__function

  def ReturnOne(self,i_bin,run,i_tag):
    print('No-Run mode')
    return 1

  def PrintMode(self,i_bin,run,i_tag):
    print(self.__mode, i_bin,run,i_tag)
    return 0

  def Function(self,i_bin,run,i_tag):

    con = configs.SetConfigurations()
    hadron = con.HadronListname(i_bin,run)
    parton = con.PartonListname(i_bin,run)  
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
  main_sub.Init(params)
  base = Base('check and run')
  function = base.GetFunction()
  n_run_total = main_sub.Sequence(params, function)
  print( 'Submission Ends.')
  print( 'Total: ', str(n_run_total)+'-jobs were submitted.')  
  print( '##################')


if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = main_sub.GetParams(argc, argvs)
  Main(params)
