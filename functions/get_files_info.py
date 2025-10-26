import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    # Join the paths
    target_path = os.path.join(working_directory, directory)
    # Get absolute versions
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(target_path)
    # Check if target starts with working directory path
    if not abs_target.startswith(abs_working + os.path.sep) and abs_target != abs_working:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'

    try:

        # Get list of items in directory
        items = os.listdir(abs_target)
        # Build list of formatted strings
        formatted_lines = []
        for item in items:
            full_item_path = os.path.join(abs_target, item) # Build the full path to this specific item
            size = os.path.getsize(full_item_path) # Use full path
            is_directory = os.path.isdir(full_item_path) # Use full path

            formatted_lines.append(f'- {item}: file_size={size} bytes, is_dir={is_directory}')

        return "\n".join(formatted_lines)
    except Exception as e:
        return f"Error: {str(e)}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
