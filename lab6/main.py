from hmac_sha_gost import hmac_hash
import datetime


def path_getter(mode):
    while True:
        try:
            path = input(f"Input path to {mode}:\n-\t")
            file = open(path)
        except Exception as err:
            print(f"Uncorrect path. {err}.")
            continue
        else:
            file.close()
            return path


def receving_mess():
    while True:
        try:
            choose = input("Iput:\n1.\tFile\n2.\tKeyboard\n-\t")
        except Exception:
            print("Input error. Try again.")
            continue
        else:
            if choose == "1":
                while True:
                    print("\nInput mess in msg.txt")
                    try:
                        file = open("msg.txt", encoding="utf-8")
                        mess = file.read()
                        file.close()
                    except Exception as er:
                        print(f"Input error. Try again.\n{er}")
                        continue
                    else:
                        break
                break
            elif choose == "2":
                while True:
                    print("\nInput mes:")
                    try:
                        mess = input("Input your message:\n-\t")
                    except Exception as er:
                        print(f"Input error. Try again.\n{er}")
                        continue
                    else:
                        break
                break
            else:
                print("Input error. Try again.")
                continue

    return mess


def menu():
    while True:

        try:
            choose = input("\n1.\tGeneration key.\n2.\tHash.\n3.\tExit.\n-\t")
        except Exception:
            print("Input error. Try again!")
            continue
        else:
            if choose == "1":  # generation key
                while True:
                    try:
                        print("\nKey generation in progress\n")
                        obj = hmac_hash()
                        key_ = obj.generation_key()
                    except Exception as err:
                        print(f"{err}")
                        continue
                    else:
                        data = str(datetime.datetime.now())[:-7].replace(":", "-")
                        with open(f"keys/key - {data}.txt", "w", encoding="utf-8") as file:
                            file.write(key_.hex())
                        print("\n\033[36mKey generated.\033[0m\n")
                        break

            elif choose == "2":  # Hash
                key_path = path_getter("key")
                with open(f"{key_path}", encoding="utf-8") as file:
                    key_ = bytes.fromhex(file.read())
                msg = receving_mess()
                while True:
                    try:
                        hash_type = input(
                            "\n1.\tSHA-256.\n2.\tSHA-512.\n3.\tGOST R 34.11-2012 (256).\n4.\tGOST R 34.11-2012 ("
                            "512).\n5.\tExit.\n-\t")
                    except Exception as err:
                        print(f"{err}")
                    else:
                        if hash_type == "1":
                            hash_ = hmac_hash().sha_(msg.encode("utf-8"), key_, 256)

                        elif hash_type == "2":
                            hash_ = hmac_hash().sha_(msg.encode("utf-8"), key_, 512)

                        elif hash_type == "3":
                            hash_ = hmac_hash().gost_stribog(msg.encode("utf-8"), key_, 256)

                        elif hash_type == "4":
                            hash_ = hmac_hash().gost_stribog(msg.encode("utf-8"), key_, 512)

                        elif hash_type == "5":
                            print("Back...")
                            break

                        print(f"\nHash\t:\t{hash_.hex()}")

            elif choose == "3":  # Exit
                print("Good bay...")
                break



menu()

# C:\Users\GEORG\Desktop\GEORG\PythonWorks\Crypto\lab6\keys\key - 2022-04-09 13-10-23.txt