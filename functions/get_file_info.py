import os

from google.genai import types

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

def get_files_info(working_directory, directory="."):
	try:
		full_path_wd=os.path.abspath(working_directory)
		target_path_wd=os.path.normpath(os.path.join(full_path_wd, directory))
		valid_dir=os.path.commonpath([full_path_wd,target_path_wd]) == full_path_wd
	
		if not valid_dir:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	
		if not os.path.isdir(target_path_wd):
			return f'Error: "{directory}" is not a directory'

		result = ""
		for content in os.listdir(target_path_wd):
			content_path = os.path.normpath(os.path.join(target_path_wd, content))
			content_size = os.path.getsize(content_path)
			is_dir = os.path.isdir(content_path)
			result += f'- {content}: file_size={content_size} bytes, is_dir={is_dir} \n'
		return f'{result}'
	except Exception as e:
		return f'Error: "{e}"'
