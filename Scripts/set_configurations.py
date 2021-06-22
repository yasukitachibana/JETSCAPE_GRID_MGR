#Singleton Pattern
import threading
import yaml

class SetConfigurations:
  _instance = None
  _lock = threading.Lock()
  __yaml_data = None
  __i_bin_max = 0

  def __init__(self):
    print('Init [SetConfigurations]')

  def __new__(cls):
    with cls._lock:
      if cls._instance is None:
        cls._instance = super().__new__(cls)
    return cls._instance

  def InitConfigs(self, config_file):
    print('Config File: ', config_file)
    with open(config_file, 'r') as ymlf:
      self.__yaml_data = yaml.safe_load(ymlf)
    #print(self.__yaml_data)

  def GetIbinMax(self):
    return self.__i_bin_max

def Main():
  a = SetConfigurations() 
  b = SetConfigurations() 
  print(a is b)  
  a.InitConfigs()
  print(a.InitConfigs() is b.InitConfigs())  

if __name__ == '__main__':
  Main()