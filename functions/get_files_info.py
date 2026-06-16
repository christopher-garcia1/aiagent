import os
from google.genai import types

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs 
        if not valid_target_dir:
         return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        items = os.listdir(target_dir)
        display_name = 'current' if target_dir == working_dir_abs else directory
        output = [f'Result for {display_name} directory']
        for item in items:
            full_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path)
            output.append(f'- {item}: file_size={size}, is_dir={is_dir}')
        return '\n'.join(output)

    except Exception as e:
       return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)