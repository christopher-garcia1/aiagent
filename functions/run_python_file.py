import os
import subprocess
from google.genai import types

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
        try:
            working_dir_abs = os.path.abspath(working_directory)
            target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
            valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs 
            if not valid_target_dir:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            if not os.path.isfile(target_dir):
                return f'Error: "{file_path}" does not exist or is not a regular file'
            if not target_dir.endswith('.py'):
                 return f'Error: "{file_path}" is not a Python file'
            command = ['python', target_dir]
            if args:
                 command.extend(args)
            results = subprocess.run(command, capture_output=True, text= True, timeout= 30,cwd=working_dir_abs)

            if results.returncode != 0:
                 return f'Process exited with code {results.returncode}'
            if not results.stderr and not results.stdout:
                 return "No output produced"
           
            output = ""

            if results.stdout:
                output += f"STDOUT:\n{results.stdout}"

            if results.stderr:
                if output:
                    output += "\n"
                output += f"STDERR:\n{results.stderr}"
            return output
  

        except Exception as e:
            return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs file in specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the file to read, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
               type = types.Type.ARRAY,
               items = types.Schema(
                    type = types.Type.STRING
               ),
               description = 'the optional argumens'
            )
        },
        required = ['file_path'],
    ),
)
