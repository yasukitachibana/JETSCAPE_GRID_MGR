import os
import sys
import set_configurations as configs
import main_submission as main_sub
import shutil
import single_run
import run_jetscape as rj
import manage_dir as mdir
import command as cmd

def Write(input, output,i_bin=''):
  con = configs.SetConfigurations()
  print('merge', input)
  print('-->', output)
  command = 'cat {} > {}'.format(input,output)
  
  if con.Que() == 'no_que' or con.Que() == 'test':
    print('no que mode')
    print('Submission, Main Command')
    print(command)
    print('-')
    os.system(command)
  else:
    log = con.LogFilename(i_bin,'M')
    err = con.ErrorFilename(i_bin,'M')    
    job = con.Jobname(i_bin,'M')
    run_command = cmd.RunCommand(command)
    master_command = cmd.MasterCommand(run_command)    
    qsub_command = cmd.QsubCommand(master_command, job, log, err)    
    print('Submission, Que:', con.Que())
    print(qsub_command)
    print('-')
    os.system(qsub_command)


def Merge():
  print( 'Start Merging')
  con = configs.SetConfigurations()

  i_bin_start = params['start']
  i_bin_end = min(params['end'], con.IbinMax())

  for i_tag, tag in enumerate(con.Tags()):
    print(i_tag, ': ', tag)
    con.SetOutdirname(i_tag)
    #print(con.MergedDirname())
    mdir.Mkdirs(con.MergedDirname())
    chmod_cmd = 'chmod -R 777 ' + con.MergedDirname()    
    print( '------------------')
    for i_bin in range(i_bin_start, i_bin_end):
      hadron = con.HadronListname(i_bin,'*')
      hadron_merged = con.MergedHadronListname(i_bin)      
      parton = con.PartonListname(i_bin,'*')
      parton_merged = con.MergedPartonListname(i_bin)      
      Write(hadron,hadron_merged,i_bin)
      print('------')
      Write(parton,parton_merged,i_bin)        
      print( '------------------')
      os.system(chmod_cmd)
  print( 'Finish Merging')
  print( '##################')

def Main(params):

  main_sub.Init(params)
  
  base = rj.Base('merge and transfer')  
  function = base.GetFunction()
  con = configs.SetConfigurations()
  con.NotificationOff()
  ##==========================
  n_run_total = main_sub.Sequence(params, function)
  print( 'Total: ', str(n_run_total)+'-jobs are incompleted.') 
  if n_run_total > 0:
    print( '--> Exit.') 
    exit()
  print( '##################')
  ##==========================
  Merge()


if __name__ == '__main__':
  argvs = sys.argv
  argc = len(argvs)
  params = main_sub.GetParams(argc, argvs)
  Main(params)
