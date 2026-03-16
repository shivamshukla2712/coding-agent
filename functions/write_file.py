import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
	try:
		full_path_wd=os.path.abspath(working_directory)
		target_file_path=os.path.normpath(os.path.join(full_path_wd, file_path))
		valid_file_path=os.path.commonpath([full_path_wd,target_file_path]) == full_path_wd
		if not valid_file_path:
			return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'	
	
		if os.path.isdir(target_file_path):
			return f'Error: Cannot write to "{target_file_path}" as it is a directory'
		
		parent_dir = os.path.dirname(target_file_path)
		# print(parent_dir)
		os.makedirs(parent_dir, exist_ok = True)		

		with open(target_file_path, "w") as f:
			f.write(content)
		
		return f'Successfully wrote to "{target_file_path}" ({len(content)} characters written)'
	
	except Exception as e:
		return f'Error: Writing to "{file_path}" failed because {e}'
