import os

def write_file(working_directory, file_path, content):
    try:
        # Build an absolute path for both
        working_directory = os.path.abspath(working_directory)

        # Join the working directory with the file path (unless it's absolute)
        if not os.path.isabs(file_path):
            file_path = os.path.join(working_directory, file_path)

        file_path = os.path.abspath(file_path)

        # Ensure the target path is inside the working directory
        if not file_path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Make sure any needed folders exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write (overwrite) the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
