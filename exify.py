import shutil
import subprocess
import os
from pathlib import Path
from time import sleep

def exify(path):
    try:

        subprocess.run(['python','-m','PyInstaller',path,'--onefile'],check=True)
        if os.path.exists(f'./{path.replace('.py','').strip('')}.exe'):
            if os.path.exists('./Previous exe versions'):
                n = len(list(Path('./Previous exe versions').rglob('*.*')))
                os.rename(f'./{path.replace('.py','').strip('')}.exe',f'./{path.replace('.py','').strip('')}{n}.exe')
                shutil.move(f'./{path.replace('.py','').strip('')}{n}.exe','./Previous exe versions')
            else:
                os.mkdir('Previous exe versions')    
                os.rename(f'./{path.replace('.py','').strip('')}.exe',f'./{path.replace('.py','').strip('')}0.exe')
                shutil.move(f'./{path.replace('.py','').strip('')}0.exe','./Previous exe versions')
        shutil.move(f'dist/{path.replace('.py','').strip('')}.exe','./')
        shutil.rmtree('build')
        shutil.rmtree('dist')
        os.remove(f'{path.replace('.py','').strip('')}.spec')
    except Exception as e:
        print(f'An error occured: {e}')
        sleep(7.5)

if __name__ == '__main__':
    path = input('Enter the path of the file to exify: ')
    exify(path) 
    