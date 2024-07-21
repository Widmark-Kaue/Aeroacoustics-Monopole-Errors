from pathlib import Path
import subprocess
from time import sleep
import datetime


#case = 'circMesh_4.5ZU'

case = 'hybrid'
tests = 'spacialSchemes_corr'

root = Path().home().joinpath('OpenFOAM', 'labcc01-v2112', 'run')

for test in root.joinpath(case, tests).iterdir():
    if not test.joinpath('log.myrhoCentralFoam').exists():
        process = subprocess.check_output(['ps', 'aux'])
        while 'myrhoCentralFoam' in str(process):
            process = subprocess.check_output(['ps', 'aux'])
        print(f'Inicio do caso: {test.name} - {datetime.datetime.now()}')
        subprocess.run([f'cd {test} && ./run.sh &'], shell=True)
        sleep(20)
