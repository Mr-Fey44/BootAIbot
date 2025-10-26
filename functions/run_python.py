import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    # Join the paths
    target_path = os.path.join(working_directory, file_path)
    # Get absolute versions
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(target_path)
    # Check if target starts with working directory path
    if not abs_target.startswith(abs_working + os.path.sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_target):
        return f'Error: File "{file_path}" not found.'\

    if not abs_target.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    #if not os.access(abs_target, os.X_OK):
    #    return f'Error: File "{file_path}" is not executable.'
    try:
            commands = ["python3", abs_target]
            if args:
                commands.extend(args)
            result = subprocess.run(
                commands,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=abs_working,
            )
            output = []
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr}")

            if result.returncode != 0:
                output.append(f"Process exited with code {result.returncode}")

            return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
