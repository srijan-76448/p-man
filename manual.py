def show_man(cmd: str):
    manual = f"""Usage:
    {cmd}
    {cmd} <operation> [...]
    {cmd} <package(s)>

Options:
    -r=TEXT-FILE                Reads the text file
    -e=TEXT-FILE                Exclude the following packages stored in a file
    -h, --help                  Shows the manual page
    -v, --version               output version information and exit"""

    print(manual)