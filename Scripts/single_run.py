import set_configurations as configs
import sys
import os
import set_xml
import manage_dir as mdir

def Run(i_bin,run):

    con = configs.SetConfigurations()
    print('run '+str(run))

    exec_name = 'runJetscape'


    set_xml.SetXml(i_bin, run)


    # eCM = int(argvs[1])
    # PPAA = argvs[2]
    # que_name = argvs[9]
    
    # outdir = os.path.join(gcom_gf_spath.GetOutputPath(),gcom_gf_spath.GetOutdirname(argc,argvs))
    # mdir.Mkdirs(outdir)
    # user_xml = gcom_gf_spath.GetUserXmlPath()

    # xml_filename = os.path.join(outdir,gcom_gf_spath.GetXmlFilename(this_bin,run))
    # sigma_filename = os.path.join(outdir,gcom_gf_spath.GetSigmaFilename(this_bin,run))
    # hadron_filename = os.path.join(outdir,gcom_gf_spath.GetHadronListFilename(this_bin,run))
    # parton_filename = os.path.join(outdir,gcom_gf_spath.GetPartonListFilename(this_bin,run))
    # out_filename = os.path.join(outdir,gcom_gf_spath.GetTestOutFilename(this_bin,run))
    # build_dir = os.path.join(outdir,gcom_gf_spath.GetBuidDirName(this_bin,run))
    
    # GetXml(argc, argvs, user_xml, xml_filename, this_bin, eCM, run)
    
    # command = gcom_gf_spath.GetCommand(code_path, build_dir, exec_name, xml_filename, out_filename, sigma_filename, hadron_filename,parton_filename)
    
    # mdir.Mkdirs(build_dir)
    
    # command_run = '"python run.py '+command+'"'
    
    # master_command = os.path.join(script_dir,'JobMaster')+' '+script_dir+' '+command_run
    # #print(master_command)
    
    # qsub_command = gcom_gf_spath.GenerateQsubCommand(gcom_gf_spath.GetJobName(this_bin,run),master_command, que_name)
    
    # #print('Submission, Main Command')
    # #print(master_command)
    # #print('-')
    # #os.system(master_command)
    # #exit()
    
    # print('Submission, Qsub Command')
    # print(qsub_command)
    # print('-')
    # os.system(qsub_command)
def GetParams(argc,argvs):
  print(argvs)
  print(argc)  

  if argc < 2:
    print('Please Input Options')
    print('\t$python main_submission.py AA [eCM] [centrality (e.g. 0-5)] [alphaS] [Qs] [take_recoil 0 or 1] [PythiaGun/PGun] [bin_start] [quename]')
    print('Please Input Options')
    print('\t$python main_submission.py PP [eCM] [centrality (e.g. 0-5)] [PythiaGun/PGun] [bin_start] [quename]')
    exit()
  
  if argvs[1] == 'PP' and argc < 7:
    print('Please Input Options')
    print('\t$python main_submission.py PP [eCM] [centrality (e.g. 0-5)] [PythiaGun/PGun] [bin_start] [quename]')
    exit()

  if argvs[1] != 'PP' and argc < 10:
    print('Please Input Options')
    print('\t$python main_submission.py AA [eCM] [centrality (e.g. 0-5)] [alphaS] [Qs] [take_recoil 0 or 1] [PythiaGun/PGun] [bin_start] [quename]')
    exit()

  print( '##################')
  print( '##################')
  print( 'system:', argvs[1] )
  print( 'eCM:', argvs[2] )   
  sys = argvs[1]
  ecm = int(argvs[2])

  cent = ''
  a_s = 0.0
  q_s = 0.0
  recoil = 0
  print( '------------------')
  if argvs[1] != 'PP':
    print( 'centrality:', argvs[3] )
    print( 'alphaS:', argvs[4] )
    print( 'Qs:', argvs[5] )
    no_yes = ['No','Yes']
    print( 'take recoil:', no_yes[int(argvs[6])] )
    print( '------------------')
    cent = argvs[3]
    a_s = float(argvs[4])
    q_s = float(argvs[5])
    recoil = int(argvs[6])

  print( 'Hard Process:', argvs[-3])
  print( 'bin:', argvs[-2])
  print( 'que:', argvs[-1])  
  
  hard = argvs[-3]
  i_bin_start = int(argvs[-2])
  que = argvs[-1]
  print( '##################')
  print( '##################')

  params = {
    'system': sys,
    'eCM': ecm,
    'centrality': cent,
    'alphas': a_s,
    'Qsw': q_s,
    'recoil': recoil,
    'hard': hard,
    'start': i_bin_start,
    'end': i_bin_start+1,
    'que': que
  }
  #print(params)
  return params

if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = GetParams(argc, argvs)
  con = configs.SetConfigurations()
  con.InitConfigs(os.getcwd(), '../Config/config.yaml', params)
  Run(params['start'],0)



