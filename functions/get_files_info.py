import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    """
    Returns a string describing the contents of a directory within the working_directory.
    Return an error string as needed.
    """

    try:
        # Build the full absolute paths
        target_path = os.path.join(working_directory, directory)
        abs_target = os.path.abspath(target_path)
        abs_working = os.path.abspath(working_directory)

        # Guardrail: Ensure target_path stays within working_directory
        if not abs_target.startswith(abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check existence and type
        if not os.path.exists(abs_target):
            return f'Error: "{directory}" does not exist'

        if not os.path.isdir(abs_target):
            return f'Error: "{directory}" is not a directory'

        # Try to list the directory contents
        try:
            entries = os.listdir(abs_target)
        except Exception as e:
            return f"Error: Unable to list directory '{directory}': {e}"

        # Build formatted output lines
        lines = []
        for name in entries:
            path = os.path.join(abs_target, name)
            try:
                is_dir = os.path.isdir(path)
                size = os.path.getsize(path)
                lines.append(f" - {name}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                lines.append(f" - {name}: Error reading file info ({e})")

        # Build final string result
        header = (
            f"Result for current directory:\n"
            if directory == "."
            else f"Result for '{directory}' directory:\n"
        )
        return header + "\n".join(lines)

    except Exception as e:
        return f"Error: Unexpected failure while listing '{directory}': {e}"

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a text file located in the working directory or a subdirectory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory."
            ),
        },
        required=["file_path"]
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the script."
            ),
        },
        required=["file_path"]
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file with the provided content in the working directory or subdirectory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file."
            ),
        },
        required=["file_path", "content"]
    ),
)