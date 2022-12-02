import socket
from utils import menu_message, challenger_message, help_message


def play_vs_computer(s: socket):
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


def play_vs_player(s: socket):
    playing = True

    while playing:
        print("Please wait for the host to pick a number.\n")
        message = s.recv(1024).decode()
        print(message)
        
        message = ""

        while message[:15] != "Congratulations":
            guess = input("Try guessing the number: ")

            if not (guess.isdigit() and int(guess) <= 50):
                print("Invalid input value. Please select an integer between 0 and 50.")
                continue

            s.send(guess.encode())
            message = s.recv(1024).decode()

            print(message)
        
        play_again = s.recv(4).decode()
        if play_again == 'n':
            print("The host has ended the match.\n")
            playing = False
        else:
            print("Starting new match...")


def run_client():
    host = socket.gethostname()
    port = 5050

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting to server...")
    client_socket.connect((host, port))
    print("Connection successfully established.\n")

    player_type = client_socket.recv(1024).decode()

    if player_type == "host":
        print(menu_message)
        
        while True:
            option = input("To select one of the options above, please type in its index: ")
            print()

            if option ==  '1':
                client_socket.send(option.encode())
                play_vs_computer(client_socket)
                continue
            elif option == '2':
                client_socket.send(option.encode())
                print("Waiting for second player to connect...")
                message = client_socket.recv(1024).decode()
                print(message)
                playing = True

                while playing:
                    number = input("Please pick a number for the second player to guess: ")
                    if not (number.isdigit() and int(number) <= 50):
                        print("Invalid input value. Please select an integer between 0 and 50.")
                        continue

                    client_socket.send(number.encode())
                    message = ""

                    while message[:37] != "The second player guessed the number!":
                        message = client_socket.recv(1024).decode()
                        print(message)

                    play_again = input("Would you like to play again? (Y/n): ").lower()
                    print()

                    while play_again not in ['y', 'n']:  
                        play_again = input("Invalid input value. Please use Y/n.\nWould you like to play again? (Y/n): ").lower()
                        print()
                    
                    client_socket.send(play_again.encode())

                    if play_again == 'n':
                        playing = False
                        print("Match ended. Going back to main menu...\n")
                        print(menu_message)
                    else:
                        print("Starting new match...")
            elif option == '3':
                print(help_message)
                continue
            elif option == '4':
                client_socket.send(option.encode())
                break
            else:
                print("The selected value is invalid.")
    else:
        print(challenger_message)
        play_vs_player(client_socket)



    print("Thank you for playing Guess The Number!\nDisconnecting...")
    client_socket.close()


if __name__ == "__main__":
    run_client()