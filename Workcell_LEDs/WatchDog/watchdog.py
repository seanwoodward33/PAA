#!/usr/bin/python3

#Import required packages
import subprocess
import re

#Array of programs and file locations to check if they are running
prog_array = [["SLASMain.py","/home/pi/Git/PAA/Workcell_LEDs/SLAS_Controller/SLASMain.py"]]

#run ps command and look for programs that are supposed to be running
result = subprocess.check_output(["ps","aux"])
for searches in prog_array:
    m = re.search("./" + searches[0], result.decode("utf_8"))
    if m == None:
        subprocess.Popen([searches[1], "&"])