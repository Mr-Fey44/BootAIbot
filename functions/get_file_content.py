import os
from functions.config import MAX_CHARS
# MAX_CHARS = 10000
from google.genai import types

def get_file_content(working_directory, file_path):
    # Join the paths
    target_path = os.path.join(working_directory, file_path)
    # Get absolute versions
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(target_path)
    # Check if target starts with working directory path
    if not abs_target.startswith(abs_working + os.path.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_target):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_target, "r") as file:
            file_content_string = file.read(MAX_CHARS)

        if len(file_content_string) == MAX_CHARS:
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string

    except Exception as e:
        return f"Error: {str(e)}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
