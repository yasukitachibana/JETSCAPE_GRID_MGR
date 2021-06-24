import set_configurations as configs
import os

def Command(i_bin,run):
  con = configs.SetConfigurations()

  cd = 'cd ' + con.BuildDirname(i_bin,run)
  cmake = CmakeCommand(con.CodePath(), con.CmakeOpt())
  make = MakeCommand(con.MakeOpt())
  exec = ExecCommand(i_bin,run)
  hadron = HadronListCommand(i_bin,run)  
  parton = PartonListCommand(i_bin,run)
  cd_rm = 'cd ../ ; rm -r ' + con.BuildDirname(i_bin,run)
  return ' ; '.join([cd,cmake,make,exec,hadron,parton,cd_rm])

def CmakeCommand(code_path, opt):
    return 'cmake '+opt+' '+code_path

def MakeCommand(opt):
    return 'make '+opt

def ExecCommand(i_bin,run):
  con = configs.SetConfigurations()
  return './'  + con.ExecRunJetscape() + ' ' + con.XmlFilename(i_bin,run) + ' ' + con.MasterXml()

def HadronListCommand(i_bin,run):
  con = configs.SetConfigurations()  
  return './FinalStateHadrons ' + con.OutputFilename(i_bin,run) + ' ' + con.HadronListname(i_bin,run)

def PartonListCommand(i_bin,run):
  con = configs.SetConfigurations()  
  return './FinalStatePartons '  + con.OutputFilename(i_bin,run) + ' ' + con.PartonListname(i_bin,run)

################################################
def CheckUpdateCommand():
  con = configs.SetConfigurations()
  command = 'python update_check.py --d {} --e {} '
  dir = con.OutputDirname()
  email = con.Email()
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
def QsubCommand(master_command, job, log, err):
  con = configs.SetConfigurations()
  head = ' '.join(['sbatch -q',con.Que(),con.QueOpt()])
  jobname = '--job-name {} -o {} -e {}  -- '.format(job, log, err)
  return ' '.join([head,jobname,master_command])
################################################

if __name__ == '__main__':
  print(MainCommand())