from functions.run_python_file import run_python_file

def main():
    print('run_python_file("calculator", "main.py"):')
    print(run_python_file("calculator", "main.py"))
    print()

    print('run_python_file("calculator", "main.py", ["3 + 5"]):')
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    print('run_python_file("calculator", "tests.py"):')
    print(run_python_file("calculator", "tests.py"))
    print()

    print('run_python_file("calculator", "../main.py"):')
    print(run_python_file("calculator", "../main.py"))
    print()

    print('run_python_file("calculator", "nonexistent.py"):')
    print(run_python_file("calculator", "nonexistent.py"))
    print()

    print('run_python_file("calculator", "lorem.txt"):')
    print(run_python_file("calculator", "lorem.txt"))
    print()

if __name__ == "__main__":
    main()
