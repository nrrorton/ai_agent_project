from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types

WORKING_DIRECTORY = "./calculator"

# Map function names to actual functions
FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call_part, verbose=False):
    # Map function names to actual functions
    func_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    fn_name = function_call_part.name
    fn_args = function_call_part.args.copy()
    fn_args["working_directory"] = "./calculator"  # always inject working directory

    if verbose:
        print(f"Calling function: {fn_name}({fn_args})")
    else:
        print(f" - Calling function: {fn_name}")

    # Filter out --verbose from LLM args if calling run_python_file
    if fn_name == "run_python_file" and "args" in fn_args:
        fn_args["args"] = [arg for arg in fn_args["args"] if arg != "--verbose"]

    if fn_name not in func_map:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=fn_name,
                response={"error": f"Unknown function: {fn_name}"}
            )]
        )

    # Call the actual function
    result = func_map[fn_name](**fn_args)

    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=fn_name,
            response={"result": result}
        )]
    )