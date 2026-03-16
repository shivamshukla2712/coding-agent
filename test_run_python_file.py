from functions.run_python_file import run_python_file

def main():
	fr = run_python_file("calculator", "main.py")
	print("Result for running 'main.py' file:")
	print(fr)

	fr = run_python_file("calculator", "main.py", ["3 + 5"])
	print("Result for 'main.py' file with args:")
	print(fr)

	fr = run_python_file("calculator", "tests.py")
	print("Result for tests.py")
	print(fr)
	
	fr = run_python_file("calculator", "../main.py")
	print("Result for '../main.py' directory:")
	print(fr)
	
	fr = run_python_file("calculator", "nonexistent.py") 
	print("Result for 'nonexistent.py' directory:")
	print(fr)

	fr = run_python_file("calculator", "lorem.txt") 
	print("Result for 'lorem.txt' directory:")
	print(fr)

main()
