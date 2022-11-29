import socket

menu_message = '''Welcome to Guess The Number!\n\n
1. Challenge Computer\n
2. Challenge Player\n
3. Help\n
4. Exit\n'''

help_message = '''This is a simple game of Guess The Number.\n
Here is how it works:\n
- you can choose to play against the computer or another player\n
- a number between 0 and 50 will then be randomly selected by the adversary\n
- on each turn, you will attempt to guess the number by typing it in\n
- for each wrong guess, you will receive a message prompting you to go higher or lower\n
- once you guess the number you will receive an according message, letting you know your current and best scores\n
- you can then choose to play again or go back to the main menu\n

That's it, now go have some fun!'''


def play(server: socket):
    return


def run_client():
    host = socket.gethostname()
    port = 5050

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting to server...")
    client_socket.connect((host, port))
    print("Connection successfully established.\n")

    print(menu_message)

    while True:
        option = input("To select one of the options above, please type in its index: ")
        print()

        if option in ['1', '2']:
            play(client_socket)
            continue
        elif option == '3':
            print(help_message)
            continue
        elif option == '4':
            client_socket.send(option.encode())
            break
        else:
            print("The selected value is invalid.")
    
    print("Thank you for playing Guess The Number!")
    client_socket.close()


if __name__ == "__main__":
    run_client()