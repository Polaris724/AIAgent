import os
import subprocess

def run_python_file(working_directory, file_path):

    abspath_wd = os.path.abspath(working_directory)
    joined_path = os.path.join(working_directory, file_path)
    abspath_joined = os.path.abspath(joined_path)

#check if file is in the working directory
    if not abspath_joined.startswith(abspath_wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
#check if file_path exists
    if not os.path.isfile(abspath_joined):
        return f'Error: File "{file_path}" not found.'
    
#check if file is a python file (ends in .py)
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
#use subprocess.run to run the file
    subprocess.run(file_path, timeout=30) #needs more work
#create a timeout of 30secs when running file
#capture both stdout and stderr
#set the working directory properly
#output stdout and stderr
#if exit code != 0, return exited with code X
#if no output produced, return "No output produced."
#catch and handle errors