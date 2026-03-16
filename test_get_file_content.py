from functions.get_file_content import get_file_content

def main():
        fc = get_file_content("calculator", "main.py")
        print("Result for 'main.py' file")
        print(fc)

        fc = get_file_content("calculator", "pkg/calculator.py")
        print("Result for 'pkg/calculator.py' file:")
        print(fc)

        fc = get_file_content("calculator", "/bin/cat")
        print("Result for '/bin/cat' directory:")
        print(fc)

        fc = get_file_content("calculator", "pkg/does_not_exist.py")
        print("Result for 'pkg/does_not_exist.py' directory:")
        print(fc)

main()
