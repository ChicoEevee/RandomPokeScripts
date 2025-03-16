import os
from os import path
import shutil
import sys

cwd = os.getcwd()

for root, dirs, files in os.walk(cwd):
    # Verifica si hay archivos .bntx en el directorio actual
    if any(file.endswith('.bntx') for file in files):
        os.system(f'C:\\Scripts\\quickbms.exe -q -K C:\\Scripts\\Switch_BNTX_SameFolder.bms "{root}" "{root}"' )

        for count, filename in enumerate(os.listdir(root)):
            if ".dds" in filename:
                print(root + filename)
                os.system('"C:\\Scripts\\Noesis\\Noesis.exe ?cmode "' + root + '\\' + filename + '" "'+ root + '\\' + filename[:-3] + 'png"')
                #os.system(f'del "{root}\\{filename}"')
