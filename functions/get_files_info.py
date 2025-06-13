import os
def get_files_info(working_directory, directory=None):
    abspath_d = os.path.abspath(directory)
    abspath_wd = os.path.abspath(working_directory)
    if os.path.isdir(abspath_d):
        if not abspath_d.startswith(abspath_wd) or directory != None:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif directory == None:
            return F'Error: No directory selected'
        else: #Create the three pieces of info with functions, append to attributes and setup output string
            attributes = []
            contents = os.listdir(directory) 
            for content in contents:
                attributes.append((contents[content], os.path.getsize(content), os.path.isdir(content)))
    else:
        return f'Error: "{directory}" is not a directory'