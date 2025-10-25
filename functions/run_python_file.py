import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if within working directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if file exists
        if not os.path.exists(abs_file_path):
            return f'Error: File "{os.path.basename(file_path)}" not found.'

        # Check if it's a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{os.path.basename(file_path)}" is not a Python file.'

        # Run the Python file
        completed = subprocess.run(
            ["python3", abs_file_path, *args],
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()

        output = ""
        if stdout:
            output += f"STDOUT:\n{stdout}\n"
        if stderr:
            output += f"STDERR:\n{stderr}\n"
        if completed.returncode != 0:
            output += f"Process exited with code {completed.returncode}\n"
        if not output.strip():
            output = "No output produced."

        return output.strip()

    except Exception as e:
        return f"Error: executing Python file: {e}"
