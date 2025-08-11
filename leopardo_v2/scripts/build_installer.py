import os
import subprocess

def build_installer():
    # Create the executable using pyinstaller
    subprocess.run([
        'pyinstaller',
        '--name=LeopardoV2',
        '--onefile',
        '--windowed',
        '--icon=../../resources/icons/leopardo.ico',
        '../../main.py'
    ])

    # Create the installer using the .iss file
    subprocess.run(['iscc', 'installer.iss'])

if __name__ == '__main__':
    build_installer()
