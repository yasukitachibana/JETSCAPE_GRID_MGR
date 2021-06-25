#Singleton Pattern
import threading
from typing import Awaitable
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
  __output_dir_path = ''
  __code_path = ''
  __original_xml = ''
  __master_xml = ''
  __output_dir_name = ''
  __n_events = 0
  __pp_or_AA = ''
  __hard = ''
  __eCM = 0
  __jloss = []
  __qsw = 0
  __t_start = ''
  __temp_end = ''  
  __qhat = 0
  __n_hydro = 0
  __alpha_s = ''
  __hydro_file_path = ''
  __cmake_opt = ''
  __make_opt = ''
  __que = ''
  __que_opt = ''
  __notification = ''
  __email = ''
  __recoil = 0

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
    self.SetOutdirname(params)

  def SetParameters(self,params): 
    self.__eCM = params['eCM']
    if params['system'] == 'PP':
      self.__pp_or_AA = 'PP'
    else:
      self.__pp_or_AA = 'AA'
      self.__hydro_file_path = self.__yaml_data['HydroFilePath'][params['eCM']].format(params['centrality'])
    self.__hard = params['hard']
    self.__qsw = params['Qsw']    
    self.__n_events = self.__yaml_data['nEvents']
    self.__output_dir_path = self.__yaml_data['OutputDirPath']
    self.__code_path = self.__yaml_data['CodePath']
    self.__original_xml = os.path.join(self.__code_path, self.__yaml_data['OriginalUserXml'][self.__pp_or_AA])
    self.__master_xml = os.path.join(self.__code_path, self.__yaml_data['MasterXml'])
    self.__run_total = self.__yaml_data['run']     
    self.__pt_hat_bins = self.__yaml_data['pthat'][params['hard']][params['eCM']]
    self.__i_bin_max = len(self.__pt_hat_bins)
    self.__jloss = self.__yaml_data['JLoss']
    self.__qhat = self.__yaml_data['qhat']
    self.__t_start = self.__yaml_data['t_start']    
    self.__temp_end = self.__yaml_data['temp_f']   
    self.__n_hydro = self.__yaml_data['nReuseHydro']   
    self.__alpha_s = params['alphas']
    self.__cmake_opt = self.__yaml_data['CMakeOption']
    self.__make_opt = self.__yaml_data['MakeOption']
    self.__que = params['que']
    self.__que_opt = self.__yaml_data['QueOptions']
    self.__recoil = params['recoil']
    self.__notification = self.__yaml_data['Notification']['OnOff']
    if self.__notification:
      self.__email = self.__yaml_data['Notification']['Email']
      print('Notification is ON. Email will be sent to', self.__email)
      print('##################')
  def SetOutdirname(self, params):
    outname = str(params['eCM'])+'_'+params['system']
    if not params['system'] == 'PP':
      outname = outname+'_'+params['centrality']+'_'+params['alphas']+'_'+params['Qsw']+'_'+str(params['recoil'])
    if not params['hard'] == 'PythiaGun':
      outname = outname+'_'+params['hard']
    self.__output_dir_name = outname

########################################################################
  def CodePath(self):
    return self.__code_path

  def OriginalXml(self):
    return self.__original_xml

  def MasterXml(self):
    return self.__master_xml

  def RunTotal(self):
    return self.__run_total

  def ScriptDir(self):
    return self.__script_dir

  def IbinMax(self):
    return self.__i_bin_max

  def PtHatBin(self):
    return self.__pt_hat_bins

  def Nevents(self):
    return self.__n_events

  def PPorAA(self):
    return self.__pp_or_AA

  def Hard(self):
    return self.__hard

  def Ecm(self):
    return self.__eCM

  def JLoss(self):
    return self.__jloss

  def AlphaS(self):
    return self.__alpha_s

  def Qsw(self):
    return float(self.__qsw)

  def Qhat(self):
    return self.__qhat

  def Tstart(self):
    return self.__t_start

  def TempF(self):
    return self.__temp_end

  def Nhydro(self):
    return self.__n_hydro

  def HydroFilePath(self):
    return self.__hydro_file_path

  def CmakeOpt(self):
    return self.__cmake_opt

  def MakeOpt(self):
    return self.__make_opt

  def Que(self):
    return self.__que

  def QueOpt(self):
    return self.__que_opt

  def Recoil(self):
    return self.__recoil

  def Notification(self):
    return self.__notification

  def Email(self):
    return self.__email


  def ExecRunJetscape(self):
    return 'runJetscape'

#########################################
  def OutputDirname(self):
    return os.path.join(self.__output_dir_path, self.__output_dir_name)

  def OutputFilename(self,i_bin,run,dat='.dat'):
    filename = 'TestOutBin{}_{}_Run{}'+dat
    filename = filename.format( str(self.__pt_hat_bins[i_bin][0]),str(self.__pt_hat_bins[i_bin][-1]),str(run) )
    return os.path.join(self.OutputDirname(), filename)

  def XmlFilename(self,i_bin,run):
    filename = 'SettingsBin{}_{}_Run{}.xml'
    filename = filename.format( str(self.__pt_hat_bins[i_bin][0]),str(self.__pt_hat_bins[i_bin][-1]),str(run) )
    return os.path.join(self.OutputDirname(), filename)

  def BuildDirname(self,i_bin,run):
    filename = 'BuildBin{}_{}_Run{}'
    filename = filename.format( str(self.__pt_hat_bins[i_bin][0]),str(self.__pt_hat_bins[i_bin][-1]),str(run) )
    return os.path.join(self.OutputDirname(), filename)
#########################################
  def HadronListname(self,i_bin,run):
    filename = 'JetscapeHadronListBin{}_{}_Run{}.out'
    filename = filename.format( str(self.__pt_hat_bins[i_bin][0]),str(self.__pt_hat_bins[i_bin][-1]),str(run) )
    return os.path.join(self.OutputDirname(), filename)

  def PartonListname(self,i_bin,run):
    filename = 'JetscapePartonListBin{}_{}_Run{}.out'
    filename = filename.format( str(self.__pt_hat_bins[i_bin][0]),str(self.__pt_hat_bins[i_bin][-1]),str(run) )
    return os.path.join(self.OutputDirname(), filename)
#########################################
  def LogDirname(self):
    return os.path.join(self.OutputDirname(), 'Log')

  def ErrorFilename(self,i_bin,run):
    filename = 'ErrorBin{}_{}_Run{}.txt'
    filename = filename.format( str(self.__pt_hat_bins[i_bin][0]),str(self.__pt_hat_bins[i_bin][-1]),str(run) )
    return os.path.join(self.LogDirname(), filename)

  def LogFilename(self,i_bin,run):
    filename = 'LogBin{}_{}_Run{}.txt'
    filename = filename.format( str(self.__pt_hat_bins[i_bin][0]),str(self.__pt_hat_bins[i_bin][-1]),str(run) )
    return os.path.join(self.LogDirname(), filename)
#########################################
  def Jobname(self,i_bin,run):
    name = 'RunBin{}_{}_Run{}'
    return name.format( str(self.__pt_hat_bins[i_bin][0]),str(self.__pt_hat_bins[i_bin][-1]),str(run) )
#########################################
  def ObsErrorFilename(self):
    filename = 'ObsError.txt'
    return os.path.join(self.LogDirname(), filename)

  def ObsLogFilename(self):
    filename = 'ObsLog.txt'
    return os.path.join(self.LogDirname(), filename)
#########################################
  def ObsJobname(self):
    return 'Obs_'+self.__output_dir_name

def Main():
  a = SetConfigurations() 
  b = SetConfigurations() 
  print(a is b)  
  a.InitConfigs()
  print(a.InitConfigs() is b.InitConfigs())  

if __name__ == '__main__':
  Main()