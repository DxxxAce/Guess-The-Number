import socket
from utils import PORT, MENU_MESSAGE, CHALLENGER_MESSAGE, HELP_MESSAGE, CONGRATS_HEADER_LENGTH, PLAYER2_WIN_HEADER_LENGTH,\
     PLAY_VS_COMPUTER, PLAY_VS_PLAYER, HELP, EXIT, FORCE_QUIT, RETURN_TO_MENU, BUFF_SIZE, LONG_BUFF_SIZE



def play_vs_computer(s: socket):
    message = ""

    while message[:CONGRATS_HEADER_LENGTH] != "Congratulations":
        guess = input("Try guessing the number: ")

        if not (guess.isdigit() and int(guess) <= 50):
            print("Invalid input value. Please select an integer between 0 and 50.")
            continue

        s.send(guess.encode())
        message = s.recv(LONG_BUFF_SIZE).decode()
        if message == FORCE_QUIT:
            return FORCE_QUIT

        print(message)


def play_vs_player(s: socket):
    playing = True

    while playing:
        print("Please wait for the host to pick a number.\n")
        message = s.recv(LONG_BUFF_SIZE).decode()
        if message in [FORCE_QUIT, RETURN_TO_MENU]:
            return message

        print(message)
        message = ""

        while message[:CONGRATS_HEADER_LENGTH] != "Congratulations":
            guess = input("Try guessing the number: ")

            if not (guess.isdigit() and int(guess) <= 50):
                print("Invalid input value. Please select an integer between 0 and 50.")
                continue

            s.send(guess.encode())
            message = s.recv(LONG_BUFF_SIZE).decode()
            if message in [FORCE_QUIT, RETURN_TO_MENU]:
                return message

            print(message)
        
        play_again = s.recv(BUFF_SIZE).decode()
        if play_again == 'n':
            print("The host has ended the match.\n")
            playing = False
        if play_again in [FORCE_QUIT, RETURN_TO_MENU]:
            return play_again
        else:
            print("Starting new match...")


def run_client():
    host = socket.gethostname()
    port = PORT

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting to server...")
    client_socket.connect((host, port))
    print("Connection successfully established.\n")

    try:
        player_type = client_socket.recv(LONG_BUFF_SIZE).decode()

        if player_type == "host":
            print(MENU_MESSAGE)
        
            while True:
                option = input("To select one of the options above, please type in its index: ")
                print()

                if option ==  PLAY_VS_COMPUTER:
                    client_socket.send(option.encode())
                    if play_vs_computer(client_socket) == FORCE_QUIT:
                        print("\nThe game session has ended abruptly.\nDisconnecting...")
                        client_socket.close()
                        return
                    continue
                elif option == PLAY_VS_PLAYER:
                    client_socket.send(option.encode())
                    print("Waiting for second player to connect...")
                    message = client_socket.recv(LONG_BUFF_SIZE).decode()
                    if message == FORCE_QUIT:
                        print("\nThe game session has ended abruptly.\nDisconnecting...")
                        client_socket.close()
                        return
                    elif message == RETURN_TO_MENU:
                        print("Second player connection terminated abruptly.\nReturning to menu...\n")
                        print(MENU_MESSAGE)
                        continue
                    print(message)
                    playing = True

                    return_to_menu = False
                    while playing:
                        number = input("Please pick a number for the second player to guess: ")
                        if not (number.isdigit() and int(number) <= 50):
                            print("Invalid input value. Please select an integer between 0 and 50.")
                            continue

                        client_socket.send(number.encode())
                        message = ""

                        while message[:PLAYER2_WIN_HEADER_LENGTH] != "The second player guessed the number!":
                            message = client_socket.recv(LONG_BUFF_SIZE).decode()
                            if message == FORCE_QUIT:
                                print("\nThe game session has ended abruptly.\nDisconnecting...")
                                client_socket.close()
                                return
                            elif message == RETURN_TO_MENU:
                                print("Second player connection terminated abruptly.\nReturning to menu...\n")
                                print(MENU_MESSAGE)
                                return_to_menu = True
                                break

                        if return_to_menu:
                            break

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
                            print(MENU_MESSAGE)
                        else:
                            print("Starting new match...")

                    if return_to_menu:
                        continue
                elif option == HELP:
                    print(HELP_MESSAGE)
                    continue
                elif option == EXIT:
                    client_socket.send(option.encode())
                    break
                else:
                    print("The selected value is invalid.")
        elif player_type == "challenger":
            print(CHALLENGER_MESSAGE)
            if play_vs_player(client_socket) == FORCE_QUIT:
                print("\nThe game session has ended abruptly.\nDisconnecting...")
                client_socket.close()
                return
        elif player_type == FORCE_QUIT:
            print("\nThe game session has ended abruptly.\nDisconnecting...")
            client_socket.close()
            return

        print("Thank you for playing Guess The Number!\nDisconnecting...")
        client_socket.close()
    except:
        option = FORCE_QUIT

        try:
            client_socket.send(option.encode())
            client_socket.close()
        except:
            print("\nThe game session has ended abruptly.\nDisconnecting...")
            return

        print("\nThe game session has ended abruptly.\nDisconnecting...")
        client_socket.close()


if __name__ == "__main__":
    run_client()