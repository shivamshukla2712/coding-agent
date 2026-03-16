import os 
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
	name= "run_python_file",
	description="Executes a specified Python file relative to the working directory",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="Path to the Python file to execute, relative to the working directory",
			),
			"args": types.Schema(
				type=types.Type.ARRAY,
				items=types.Schema(type=types.Type.STRING),
				description="List of arguments to pass to the Python file",
			),
		},
	),
)

def run_python_file(working_directory, file_path, args = None):
	try:
		full_path_wd=os.path.abspath(working_directory)
		target_file_path=os.path.normpath(os.path.join(full_path_wd, file_path))
		valid_file_path=os.path.commonpath([full_path_wd,target_file_path]) == full_path_wd
		
		if not valid_file_path:
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
		
		if not os.path.isfile(target_file_path):
			return f'Error: "{file_path}" does not exist or is not a regular file' 
		
		if not target_file_path.endswith('.py'):
			return f'Error: "{file_path}" is not a Python file' 

		command = ["python", target_file_path]

		if args:
			command.extend(args)

		completed_process = subprocess.run(command, cwd = full_path_wd, capture_output = True, text = True, timeout = 30)
		
		output_string = ""
		if completed_process.returncode != 0:
			output_string += f'Process exited with code {completed_process.returncode}\n'
		
		if not completed_process.stdout and not completed_process.stderr:
			output_string += 'No output produced'
			return output_string
		
		if completed_process.stdout:
			output_string += f'STDOUT: {completed_process.stdout}\n'
		
		if completed_process.stderr:
			output_string += f'STDERR: {completed_process.stderr}\n'

		return output_string
	
	except Exception as e:
		return f'Error: error executing file "{file_path}" due to {e}'		
