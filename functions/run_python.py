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
    
#check if file is a python file
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
#catch and handle errors
    try:
        output = []

        #use subprocess.run to run the file
        result = subprocess.run(["python3", abspath_joined], timeout=30, capture_output=True, cwd=abspath_wd)

        #output stdout and stderr
        stderr_output = result.stderr.decode("utf-8")
        stdout_output = result.stdout.decode("utf-8")
        output.append(f"STDOUT: {stdout_output}")
        output.append(f"STDERR: {stderr_output}")

        #if exit code != 0, return exited with code X
        exit_code = result.returncode
        if exit_code != 0:
            output.append(f"Process exited with code {exit_code}.")

        #if no output produced, return "No output produced."
        if result == None:
            return f"No output produced."
        else:
            return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"