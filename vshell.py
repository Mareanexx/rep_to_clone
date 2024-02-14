from pickletools import stringnl
import zipfile
import sys


global depth
def read_args():
    args = []
    for arg in sys.argv[1:]:
        args.append(arg)
    return args


def vshell(zip_file):

    zip_file = zipfile.ZipFile(zip_file)
    addresses = zip_file.namelist()
    directory = ""
    depth = 0

    while True:

        command = input("marianna:~$ ")
        if command == "exit":
            break

        elif command == "pwd": #команда для вывода полного пути до текущей директории

            if directory == "":
                print("/")

            else:
                print("/" + directory)

        elif command.split()[0] == "cd": #команда для путешествия по директориям
            try:
                if command.split()[1] == "..": #перейти на один уровень выше (директория выше)
                    if directory == "":
                        depth = 0
                        continue
                    else:
                        temp = directory.split('/')
                        directory = directory[:-len(temp[-1]) - 1]
                        depth -= 1
                elif command.split()[1] == "~": #перейти в домашний каталог
                    directory = "" 
                    depth = 0
                else:
                    check = command.split()[1][1:] + "/"
                    if not check in addresses:
                        print("sh: cd: can't cd to ", command.split()[1], ": No such file or directory")
                    else:
                        destination = command.split()[1]
                        if destination.startswith('/'):
                            directory = destination[1:]
                            depth = len(directory.split('/'))
                        else:
                            if directory:
                                directory += '/' + destination
                            else:
                                directory = destination
                            depth += 1

            except:
                print("sh: cd: can't cd to ", command.split()[1], ": No such file or directory")

        elif command.split()[0] == 'cat': #команда для вывода содержимого файла
            try:
                if(command.split()[1][0] == "/"):
                    print(zip_file.read(command.split()[1][1:]).decode())

                else:
                    if (directory == ""):
                        print(zip_file.read(command.split()[1]).decode())
                    else:
                        print(zip_file.read(directory + '/' + command.split()[1]).decode())

            except:
                print("cat: can't open '", command.split()[1], "': No such file or directory")

        elif command == "ls": #команда вывода содержимого директории
            temp_address = []
            temp_address_full = []
            for address in addresses:
                if ((len(address.split("/")) == depth+2 and "." not in address)):
                    temp_address.append(address.split("/")[-2])
                    temp_address_full.append(address)
                if ((len(address.split("/")) == depth+1) and "." in address):
                    temp_address.append(address.split("/")[-1])
                    temp_address_full.append(address)


            if (directory == ""):
                for temp in temp_address:
                    print(temp)
            else:
                for temp in range(len(temp_address)):
                    if (directory.split("/")[-1] == temp_address_full[temp].split("/")[depth-1]):
                        print(temp_address[temp])

        else:
            print("sh: ", command, ": not found")


def main(args):
        zip_file = args[0]
        print(zip_file)
        vshell(zip_file)


if __name__ == '__main__':
    main(read_args())

