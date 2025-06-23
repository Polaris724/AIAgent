import os

def write_file(working_directory, file_path, content):
    
    abspath_wd = os.path.abspath(working_directory)
    joined_path = os.path.join(working_directory, file_path)
    abspath_joined = os.path.abspath(joined_path)
    
    #check fle_path in working_directory
    if not abspath_joined.startswith(abspath_wd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    #check if file_path exists
    create_write_status = "w"
    if not os.path.exists(abspath_joined):
        #if it doesn't, create it
        os.makedirs(os.path.dirname(abspath_joined), exist_ok=True)
        create_write_status = "x"
        
    #overwrite contents of the file with 'content' argument
    try:
        with open(abspath_joined, create_write_status) as f:
            f.write(content)
        #if successful, return a feedback string
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    #catch errors and handle them throughout the process
    except Exception as e:
        return f"Error: {str(e)}"
