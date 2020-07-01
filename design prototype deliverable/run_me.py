"""
Customize My Rig's Setup and Startup

References:
- https://www.tutorialspoint.com/How-are-files-extracted-from-a-tar-file-using-Python
- https://stackoverflow.com/questions/4419752/how-to-run-python-setup-py-install-from-within-python
"""


import tarfile
import subprocess


cmr = tarfile.open('customize-my-rig.tar.gz')
cmr.extractall('')
cmr.close()

subprocess.call(['python3','customize-my-rig/setup.py','install'])
subprocess.call(['python3','customize-my-rig/manage.py','runserver'])