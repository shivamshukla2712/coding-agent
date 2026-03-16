from functions.write_file import write_file

def main():
        fw = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print("Result for write on 'lorem.txt'")
        print(fw)

        fw = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print("Result for write on 'morelorem.txt' file:")
        print(fw)

        fw = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print("Result for write on 'tmp/tempt.txt' file:")
        print(fw)

main()
