import os
def get_files_info(working_directory, directory=None):
    if directory == None:
        return F'Error: No directory selected'
    
    abspath_d = os.path.abspath(directory)
    abspath_wd = os.path.abspath(working_directory)
    joined_path = os.path.join(working_directory, directory)
    absjoined_path = os.path.abspath(joined_path)

    if not absjoined_path.startswith(abspath_wd):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(absjoined_path):
        return f'Error: "{directory}" is not a directory'
    result = ""
    try:
        contents = os.listdir(absjoined_path)
        for content in contents:
            file_path = os.path.join(absjoined_path, content)
            result += f"- {content}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"