"""
Customize My Rig's Setup and Startup

References:
- https://www.tutorialspoint.com/How-are-files-extracted-from-a-tar-file-using-Python
- https://stackoverflow.com/questions/4419752/how-to-run-python-setup-py-install-from-within-python
- https://stackoverflow.com/questions/60678697/error-loading-python-lib-with-pyinstaller-on-macos
- https://stackoverflow.com/questions/7225900/how-to-install-packages-using-pip-according-to-the-requirements-txt-file-from-a
"""


import tarfile
import subprocess


cmr = tarfile.open('customize-my-rig.tar.gz')
cmr.extractall('')
cmr.close()

subprocess.call(['pip','install','requests'])
subprocess.call(['pip','install','bs4'])
subprocess.call(['python3','customize-my-rig/setup.py','install'])
subprocess.call(['python3','customize-my-rig/manage.py','runserver'])