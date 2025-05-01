import set_configurations as configs
import os

def Command(i_bin,run):
  con = configs.SetConfigurations()

  cd = 'cd ' + con.BuildDirname(i_bin,run)
  cmake = CmakeCommand(con.CodePath(), con.CmakeOpt(), con.ContainerPath())
  make = MakeCommand(con.MakeOpt(), con.ContainerPath())
  exec = ExecCommand(i_bin,run)
  hadron = HadronListCommand(i_bin,run)  
  parton = PartonListCommand(i_bin,run)
  cd_rm = 'cd ../ ; rm -r ' + con.BuildDirname(i_bin,run)
  return ' ; '.join([cd,cmake,make,exec,hadron,parton,cd_rm])

def ExecContainer(container_path):
    return 'singularity exec {}'.format(container_path)

def CmakeCommand(code_path, opt, container_path):
    exec_container_command = ExecContainer(container_path)
    return '{} cmake {} {}'.format(exec_container_command, opt, code_path)
    # return 'cmake {} {}'.format(opt, code_path)
    # return 'cmake '+opt+' '+code_path

def MakeCommand(opt, container_path):
    exec_container_command = ExecContainer(container_path)  
    return '{} make {}'.format(exec_container_command, opt)
    #return 'make {}'.format(opt)

def ExecCommand(i_bin,run):
  con = configs.SetConfigurations()
  exec_container_command = ExecContainer(con.ContainerPath())
  return exec_container_command + ' ./'  + con.ExecRunJetscape() + ' ' + con.XmlFilename(i_bin,run) + ' ' + con.MasterXml()

def HadronListCommand(i_bin,run):
  con = configs.SetConfigurations()  
  exec_container_command = ExecContainer(con.ContainerPath())
  return exec_container_command + ' ./FinalStateHadrons ' + con.OutputFilename(i_bin,run) + ' ' + con.HadronListname(i_bin,run)

def PartonListCommand(i_bin,run):
  con = configs.SetConfigurations()  
  exec_container_command = ExecContainer(con.ContainerPath())
  return exec_container_command + ' ./FinalStatePartons '  + con.OutputFilename(i_bin,run) + ' ' + con.PartonListname(i_bin,run)

def MergeCommand( que = 'no_que'):
  con = configs.SetConfigurations()
  command = ' '.join(['python', 'merge_and_transfer.py', con.System(), str(con.Ecm())])
  if not con.System() == 'PP':
    command = ' '.join([command, con.Centrality(), str(con.AlphaS()), str(con.Qsw()), str(con.Recoil())])
  command = ' '.join([command, con.Hard(), str(con.IBinStart()), str(con.IBinEnd()), que])
  return command

def ExtractSigmaCommand(output,sigmafile,run_start,run_end,mergedsigmafile):
  return 'python create_sigma_file.py {} {} {} {} {}'.format(output,sigmafile,run_start,run_end,mergedsigmafile)


################################################
def CheckUpdateCommand(end_command = None):
  con = configs.SetConfigurations()
  command = 'python update_check.py {} {}'
  dir = con.OutputDirname()
  email = con.Email()
  if not end_command == None:
    command = ' '.join([command,end_command])
  return command.format(dir,email)
################################################
def RunCommand(command):
  return '"python run.py '+command+'"'

def MasterCommand(run_command):
  con = configs.SetConfigurations() 
  script_dir = con.ScriptDir()
  job_master = os.path.join(script_dir,'JobMaster')
  return ' '.join([job_master,script_dir,run_command])
################################################
def QsubCommand(master_command, job, log, err, que_opt = None):
  con = configs.SetConfigurations()
  if que_opt == None: 
    que_opt = con.QueOpt()
  head = ' '.join(['sbatch -q',con.Que(),que_opt])
  jobname = '--job-name {} -o {} -e {}  -- '.format(job, log, err)
  return ' '.join([head,jobname,master_command])
################################################

# if __name__ == '__main__':
#   print(MainCommand())