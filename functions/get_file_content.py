import os
def get_file_content(working_directory, file_path):
    #create absolute paths of working_directory and file_path
    abspath_wd = os.path.abspath(working_directory)
    joined_path = os.path.join(working_directory, file_path)
    abspath_joined = os.path.abspath(joined_path)
    
    #use absolute paths and .startswith() to determine if file_path resides in workking_directory
    if not abspath_joined.startswith(abspath_wd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    #check if file is a file
    if not os.path.isfile(abspath_joined):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    #check length of file, if characters > 10,000, truncate with note at end
    #as always, catch and handle errors throughout the process
    try:
        MAX_CHARS = 10000
        with open(abspath_joined, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == 10000:
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"
