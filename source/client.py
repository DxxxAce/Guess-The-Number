import socket
from utils import menu_message, help_message


def play(s: socket):
    message = ""

    while message[:15] != "Congratulations":
        guess = input("Try guessing the number: ")

        if not (guess.isdigit() and int(guess) <= 50):
            print("Invalid input value. Please select an integer between 0 and 50.")
            continue

        s.send(guess.encode())
        message = s.recv(1024).decode()

        print(message)

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
            client_socket.send(option.encode())
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
    
    print("Thank you for playing Guess The Number!\nDisconnecting...")
    client_socket.close()


if __name__ == "__main__":
    run_client()