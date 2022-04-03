import body



def menu():
    while True:
        try:
            choice = int(input("Choose encoding:\n1.\tBASE64\n2.\tBASE32\n3.\tExit\n-\t"))
        except Exception:
            print("\nIncorrect input. Try again!\n")
            continue
        else:
            if choice == 1:
                print("\nENCODING\tBASE64\n")
                while True:
                    try:
                        ch = int(input("Choose:\n1.\tEncode\n2.\tDecode\n3.\tExit\n-\t"))
                    except Exception:
                        print("\nIncorrect input. Try again!\n")
                        continue
                    else:
                        if ch == 1:
                            body.encode_BASE64(Receving_mes())
                        elif ch == 2:
                            body.decode_BASE64(Receving_mes())
                        elif ch == 3:
                            break
                        else:
                            print("\nIncorrect input. Try again!\n")
                            continue
            elif choice == 2:
                print("\nENCODING\tBASE32\n")
                while True:
                    try:
                        ch = int(input("Choose:\n1.\tEncode\n2.\tDecode\n3.\tExit\n-\t"))
                    except Exception:
                        print("\nIncorrect input. Try again!\n")
                        continue
                    else:
                        if ch == 1:
                            body.encode_BASE32(Receving_mes())
                        elif ch == 2:
                            body.decode_BASE32(Receving_mes())
                        elif ch == 3:
                            break
                        else:
                            print("\nIncorrect input. Try again!\n")
                            continue
            elif choice == 3:
                break
            else:
                print("\nIncorrect input. Try again!\n")
                continue


def Receving_mes():
    while True:
        try:
            choice = int(input("Choose way:\n1.\tKeyboard\n2.\tFrom file\n-\t"))
        except Exception:
            print("\nIncorrect input. Try again!\n")
            continue
        else:
            if choice == 1:
                try:
                    mes = input("Input your message:\n-\t")
                except Exception:
                    print("\nIncorrect input. Try again!\n")
                    continue
                else:
                    break
            elif choice == 2:
                while True:
                    try:
                        path = input("Input path to file:\n-\t")
                        with open(path, encoding="utf-8") as file:
                            mes = ""
                            for line in file:
                                if line.count("=")>=10:
                                    continue
                                else:
                                    mes+=line
                    except Exception as er:
                        print(f"\nIncorrect input. Try again! ({er})\n")
                        continue
                    else:

                            break
                break
            else:
                print("\nIncorrect input. Try again!\n")
                continue
    return mes

menu()

"C:\\Users\\GEORG\\Desktop\\GEORG\\PythonWorks\\Crypto\\lab2\\test.txt"
