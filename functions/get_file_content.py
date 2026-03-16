import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads the content of a specified file relative to the working directory upto max of {MAX_CHARS} characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
	try:
		full_path_wd=os.path.abspath(working_directory)
		target_file_path=os.path.normpath(os.path.join(full_path_wd, file_path))
		valid_file_path=os.path.commonpath([full_path_wd,target_file_path]) == full_path_wd
		if not valid_file_path:
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'	
		
		
		if not os.path.isfile(target_file_path):
			return f'Error: File not found or is not a regular file: "{file_path}"'
		
		content = ""
		with open(target_file_path, "r") as f:
			file_content_string = f.read(MAX_CHARS)
			content += file_content_string
			if f.read(1):
				content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
		return content		
	except Exception as e:
		return f'Error: Eror reading the file "{file_path}" contents : "{e}"'

