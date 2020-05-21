import subprocess
import sys
import paramiko
import time

HOSTNAME = ""
PORT = 22
USERNAME = ""
PASSWORD = ""

PROJECT_NAME = "coins" ## substring in builds to search for

## used to get latest build in output of ls
def indexContainsSubstring(l, ss):
    for i,s in enumerate(l):
        if ss in s:
            return i
    return -1

def getBuild(inData):
    output = inData.readlines()
    outputDesc = output[::-1] ## order builds by greatest (latest)

    ind = indexContainsSubstring(outputDesc, PROJECT_NAME)
    
    return outputDesc[ind].rstrip()

def connectAndRun(cmd):
    con = paramiko.SSHClient()
    con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    con.connect(HOSTNAME, PORT, USERNAME, PASSWORD)
    
    (stdin, stdout, stderr) = con.exec_command(cmd)

    if con:
        con.close()

    return stdout;

def main():
    cmd1 = "cd /location/of/builds/" + PROJECT_NAME + ";ls;" 
    cmdOutput = connectAndRun(cmd1)
    buildFname = getBuild(cmdOutput)

    cmd2 = "cd /location/of/builds/" + buildFname; + "commands_to_exec"
    cmdOutput = connectAndRun(cmd2)
    

main()