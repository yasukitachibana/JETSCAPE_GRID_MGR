#Singleton Pattern
import threading
import yaml
import os

class SetConfigurations:
  _instance = None
  _lock = threading.Lock()
  __yaml_data = None
  __run_total = 0
  __i_bin_max = 0
  __pt_hat_bins = []
  __script_dir = ''

  def __init__(self):
    pass

  def __new__(cls):
    with cls._lock:
      if cls._instance is None:
        cls._instance = super().__new__(cls)
    return cls._instance

  def InitConfigs(self, script_dir, config_file, params):
    self.__script_dir = script_dir
    print('Config File: ', config_file)
    with open(config_file, 'r') as ymlf:
      self.__yaml_data = yaml.safe_load(ymlf)
    self.SetParameters(params)

  def SetParameters(self,params):
    self.SetRunTotal()
    self.SetPtHatBins(params['hard'],params['eCM'])

  def SetPtHatBins(self, hard, ecm):
    self.__pt_hat_bins = self.__yaml_data['pthat'][hard][ecm]
    self.__i_bin_max = len(self.__pt_hat_bins)

    #print(self.__pt_hat_bins)

  def SetRunTotal(self):
    self.__run_total = self.__yaml_data['run']

  def RunTotal(self):
    return self.__run_total

  def ScriptDir(self):
    return self.__script_dir


  def IbinMax(self):
    return self.__i_bin_max

  def PtHatBin(self):
    return self.__pt_hat_bins



def Main():
  a = SetConfigurations() 
  b = SetConfigurations() 
  print(a is b)  
  a.InitConfigs()
  print(a.InitConfigs() is b.InitConfigs())  

if __name__ == '__main__':
  Main()