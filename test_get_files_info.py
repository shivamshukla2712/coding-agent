
from functions.get_file_info import get_files_info

def main():
	fc = get_files_info("calculator", ".")
	print("Result for current directory:")
	print(fc)

	fc = get_files_info("calculator", "pkg")
	print("Result for 'pkg' directory:")
	print(fc)

	fc = get_files_info("calculator", "/bin") 
	print("Result for '/bin' directory:")	
	print(fc)

	fc = get_files_info("calculator", "../")
	print("Result for '../' directory:")	
	print(fc)

main()
