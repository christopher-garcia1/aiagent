import os 
from google.genai import types

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs 
        if not valid_target_dir:
         return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_dir, 'r') as file:
           content = file.read(10000)
           if file.read(1):
              content += f'[...File "{file_path}" truncated at 10000 characters]'
           return content
  

    except Exception as e:
       return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves content of file in specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the file to read, relative to the working directory (default is the working directory itself)",
            ),
        },
        required = ['file_path'],
    ),
)