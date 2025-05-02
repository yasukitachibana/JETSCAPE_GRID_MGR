import set_configurations as configs
import sys
import os
import xml.etree.ElementTree as ET
import edit_xml as exml
import random
import main_submission as main_sub


def SetXml(i_bin,run,i_tag):
  con = configs.SetConfigurations()
  ex = exml.EditXml()
  ex.ReadXml(con.OriginalXml())
  SetXmlGeneral(i_bin,run)
  SetXmlHard(i_bin,run,i_tag)
  SetXmlEloss(i_bin,run)
  SetXmlMedium(i_bin,run)
  ex.PrintXml(con.XmlFilename(i_bin,run))

#######################################################
# XML for Jet Energy Loss
#---
def SetXmlVacuumBrick(i_bin,run):
  con = configs.SetConfigurations()
  ex = exml.EditXml()
  ex.DeleteElement('./IS')
  ex.DeleteElement('./Preequilibrium')  
  ex.DeleteElement('./Hydro')

def SetXmlMediumInput(i_bin,run):
  con = configs.SetConfigurations()
  ex = exml.EditXml()
  print(con.HydroFilePath())
  ex.DeleteElement('./IS/Trento')
  ex.DeleteElement('./Preequilibrium/FreestreamMilne')  
  ex.DeleteElement('./Hydro/Brick')
  ex.DeleteElement('./Hydro/MUSIC')  
  ex.DeleteElement('./Hydro/CLVisc')    
  ####################################
  ex.EditParams('./IS/initial_profile_path', con.HydroFilePath())  
  ex.EditParams('./Preequilibrium/NullPreDynamics', ' ')  
  ex.EditParams('./Hydro/hydro_from_file/name', 'Hydro from file ')   
  ex.EditParams('./Hydro/hydro_from_file/read_in_multiple_hydro', 1)   
  ex.EditParams('./Hydro/hydro_from_file/hydro_files_folder', con.HydroFilePath()) 
  ##
  hydro_type = con.HydroType()
  for h_type in hydro_type:
    xpath = './Hydro/hydro_from_file/' + h_type[0]
    ex.EditParams(xpath, h_type[1]) 
  ####################################


def SetXmlMedium(i_bin,run):
  con = configs.SetConfigurations()
  if con.PPorAA() == 'PP':
    SetXmlVacuumBrick(i_bin,run)
  else:
    SetXmlMediumInput(i_bin,run)
#######################################################

#######################################################
# XML for Jet Energy Loss
#---
def SetXmlMatter(i_bin,run,q0):
  con = configs.SetConfigurations()  
  ex = exml.EditXml()
  ###################################  
  qhat_type = con.Qhat()
  # ###################################
  if q0 == '1.0':
    print('Matter')
    ex.DeleteElement('./Eloss/Lbt')
    ex.DeleteElement('./Eloss/Martini')  
    ex.DeleteElement('./Eloss/AdSCFT')    
  ###################################
  ex.EditParams('./Eloss/Matter/name', 'Matter')   
  # ex.EditParams('./Eloss/Matter/useHybridHad', 0)  
  ex.EditParams('./Eloss/Matter/matter_on', 1)    
  ex.EditParams('./Eloss/Matter/Q0', q0)
  ex.EditParams('./Eloss/Matter/T0', con.TempF())  
  ex.EditParams('./Eloss/Matter/vir_factor', '0.25')  
  ex.EditParams('./Eloss/Matter/in_vac', 0)
  ex.EditParams('./Eloss/Matter/recoil_on', 1)
  ex.EditParams('./Eloss/Matter/broadening_on', con.MatterBroadening())
  ex.EditParams('./Eloss/Matter/brick_med', 0)    
  ex.EditParams('./Eloss/Matter/hydro_Tc', con.TempF())    
  ###################################
  ex.EditParams('./Eloss/Matter/QhatParametrizationType', qhat_type)
  ex.EditParams('./Eloss/Matter/qhat0', '-2.0')
  ex.EditParams('./Eloss/Matter/alphas', con.AlphaS())
  ###################################
  ex.EditParams('./Eloss/Matter/qhatA', '10.0')
  ex.EditParams('./Eloss/Matter/qhatB', '100.0')
  ex.EditParams('./Eloss/Matter/qhatC', '0.2')
  ex.EditParams('./Eloss/Matter/qhatD', '5.0')
  ###################################

#---
def SetXmlLBT(i_bin,run):
  con = configs.SetConfigurations()  
  ex = exml.EditXml()  
  ###################################
  ex.EditParams('./Eloss/Lbt/name', 'Lbt')   
  ex.EditParams('./Eloss/Lbt/Q0', str(con.Qsw()) ) 
  ex.EditParams('./Eloss/Lbt/in_vac', 0)
  ex.EditParams('./Eloss/Lbt/only_leading', 0)  
  ex.EditParams('./Eloss/Lbt/hydro_Tc', con.TempF())    
  ###################################
  ex.EditParams('./Eloss/Lbt/alphas', con.AlphaS())
  ###################################
  if con.Qhat() == 0:
      ex.EditParams('./Eloss/Lbt/run_alphas', 0)
  else:
      ex.EditParams('./Eloss/Lbt/run_alphas', 1)
  ###################################

def SetXmlMatterLBT(i_bin,run):
  print('Matter+LBT')
  con = configs.SetConfigurations()  
  ex = exml.EditXml()
  SetXmlMatter(i_bin,run,str(con.Qsw()))
  SetXmlLBT(i_bin,run)

def SetXmlMatterMartini(i_bin,run):
  print('Matter+Martini')
  print('Under Construction. Exit.')  
  exit()
#---
def SetXmlAAjet(i_bin,run):

  con = configs.SetConfigurations()  
  ex = exml.EditXml()
  ###################################  
  ex.EditParams('./setReuseHydro', 'true')
  ex.EditParams('./nReuseHydro', con.Nhydro())  
  ###################################  
  ex.EditParams('./Eloss/tStart', con.Tstart())
  ex.EditParams('./Eloss/mutex', 'ON')    
  ###################################

  if (con.JLoss()[0] == 'Matter') and ((len(con.JLoss()) == 1) or (con.Qsw() < 0 )):
    SetXmlMatter(i_bin,run,'1.0')
  elif (con.JLoss()[0] == 'Matter') and (con.JLoss()[1] == 'LBT'):
    SetXmlMatterLBT(i_bin,run)
  elif (con.JLoss()[0] == 'Matter') and (con.JLoss()[-1] == 'Martini'):
    SetXmlMatterMartini(i_bin,run)
  else:
    print(con.JLoss()[0],'+',con.JLoss()[1])
    print('Exit.')  
    exit()
#---
def SetXmlPPjet(i_bin,run):
  ex = exml.EditXml()
  ###################################  
  ex.DeleteElement('./Eloss/Lbt')
  ex.DeleteElement('./Eloss/Martini')  
  ex.DeleteElement('./Eloss/AdSCFT')    
  ###################################
  ex.EditParams('./Eloss/Matter/Q0', '1.0')
  ex.EditParams('./Eloss/Matter/in_vac', 1)
  ex.EditParams('./Eloss/Matter/vir_factor', '0.25')
  ex.EditParams('./Eloss/Matter/recoil_on', 1)
  ex.EditParams('./Eloss/Matter/broadening_on', 0)
  ex.EditParams('./Eloss/Matter/brick_med', 0)
  ###################################     
#---
def SetXmlEloss(i_bin,run):
  con = configs.SetConfigurations()
  ex = exml.EditXml()
  ###################################
  ex.EditParams('./Eloss/deltaT', '0.1')
  ex.EditParams('./Eloss/formTime', '-0.1')
  ex.EditParams('./Eloss/maxT', '250')
  ###################################  
  ex.EditParams('./JetHadronization/name', 'colorless')
  ex.EditParams('./JetHadronization/take_recoil', con.Recoil() )
  ex.EditParams('./JetHadronization/eCMforHadronization', int(0.5*con.Ecm()) )  
  ###################################  
  if con.PPorAA() == 'PP':
    SetXmlPPjet(i_bin,run)
  else:
    SetXmlAAjet(i_bin,run)
#######################################################

#######################################################
# XML for Hard Process
#---
def SetXmlHard(i_bin,run,i_tag):
  con = configs.SetConfigurations()
  if con.Hard() == 'PythiaGun':
    SetXmlPythiaGun(i_bin,run,i_tag)
  elif con.Hard() == 'PGun':
    SetXmlPGun(i_bin,run,i_tag)

def SetXmlPythiaGun(i_bin,run,i_tag=0):
  con = configs.SetConfigurations()
  ex = exml.EditXml()  
  ex.DeleteElement('./Hard/PGun')
  ex.EditParams('./Hard/PythiaGun/name', 'PythiaGun')
  ex.EditParams('./Hard/PythiaGun/eCM', con.Ecm())  
  ex.EditParams('./Hard/PythiaGun/pTHatMin', con.PtHatBin()[i_bin][0])
  ex.EditParams('./Hard/PythiaGun/pTHatMax', con.PtHatBin()[i_bin][1])  
  # ex.EditParams('./Hard/PythiaGun/useHybridHad', 0)
  ex.EditParams('./Hard/PythiaGun/FSR_on', 0)

def SetXmlPGun(i_bin,run,i_tag):
  con = configs.SetConfigurations()
  ex = exml.EditXml()  
  ex.DeleteElement('./Hard/PythiaGun')
  ex.EditParams('./Hard/PGun/name', 'PGun')  
  ex.EditParams('./Hard/PGun/pT', con.PtHatBin()[i_bin][0])
  parID = 0
  if con.Tags()[i_tag] == 'quark':
    parID = 1
  elif con.Tags()[i_tag] == 'gluon':
    parID = 21
  ex.EditParams('./Hard/PGun/parID', parID)
  # ex.EditParams('./Hard/PGun/useHybridHad', 0)
#######################################################


#######################################################
# XML for JETSCAPE framework
#---
def SetXmlGeneral(i_bin,run):
  con = configs.SetConfigurations()
  ex = exml.EditXml()

  output_filename = con.OutputFilename(i_bin,run,dat='')

  random_int = run
  if con.RandomRandomSeed() == 1:
    random_int = 0
  elif con.RandomRandomSeed() == 2:
    random_int = random.randint(1,1000*con.RunTotal()*con.Nevents()+1)

  ex.DeleteElement('./JetScapeWriterHepMC')
  ###########################################
  ex.EditParams('./JetScapeWriterAscii','on')
  ex.EditParams('./outputFilename',output_filename)  
  ex.EditParams('./JetScapeWriterFinalStatePartonsAscii','off')
  ex.EditParams('./JetScapeWriterFinalStateHadronsAscii','off')
  ex.EditParams('./vlevel',0)
  ex.EditParams('./nEvents',con.Nevents())
  ex.EditParams('./nEvents_printout',1)
  ex.EditParams('./Random/seed',random_int)  
  ###########################################  
  #ex.PrintXml('test.xml')
#######################################################

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = main_sub.GetParams(argc, argvs)  
  con = configs.SetConfigurations()
  params['end'] = params['start']+1
  con.InitConfigs(os.getcwd(), params['yaml'], params)
  SetXml(params['start'],0)



