import os

def Mkdirs(path):
    if not os.path.isdir(path):
        print('creating "'+path+'" directory')
        os.makedirs(path)

def IsEmpty(path):
    files = os.listdir(path)
    files = [f for f in files if not f.startswith(".")]
    if not files:
        return True
    else:
        return False
