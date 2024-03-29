import socket
from utils import PORT, STARTING_SCORE, STARTING_GUESS, SCORE_PER_GUESS, BUFF_SIZE, LONG_BUFF_SIZE,\
    PLAY_VS_COMPUTER, PLAY_VS_PLAYER, EXIT, FORCE_QUIT, RETURN_TO_MENU, generate_random_number


def play_vs_computer(s: socket, high_score) -> int:
    number = generate_random_number()
    guess = STARTING_GUESS
    score = STARTING_SCORE

    while guess != number:
        guess = int(s.recv(BUFF_SIZE).decode())
        if guess == FORCE_QUIT:
            return FORCE_QUIT

        score -= SCORE_PER_GUESS if score > 0 else 0
        message: str

        if guess == number:
            high_score = score if score > high_score else high_score
            message = f"Congratulations, you have guessed the number!\nCurrent Score: {score}\nHigh Score: {high_score}\n"
            print(f"Game ended. Player finished with a score of {score}.\n")
        elif (guess > number):
            message = "Your guess is too high. Try going lower!\n"
        else:
            message = "Your guess is too low. Try going higher!\n"

        s.send(message.encode())

    return high_score


def play_vs_player(s1: socket, s2: socket):
    high_score = 0
    playing = True

    while playing:
        message = s1.recv(LONG_BUFF_SIZE).decode()
        if message == FORCE_QUIT:
            s2.send(message.encode())
            return FORCE_QUIT
        
        number = int(message)
        guess = STARTING_GUESS
        score = STARTING_SCORE

        message = "The host is done picking."
        s2.send(message.encode())

        while guess != number:
            message = s2.recv(BUFF_SIZE).decode()
            if message == FORCE_QUIT:
                message = RETURN_TO_MENU
                s1.send(message.encode())
                return RETURN_TO_MENU

            guess = int(message)

            score -= SCORE_PER_GUESS if score > 0 else 0
            message1: str
            message2: str

            if guess == number:
                high_score = score if score > high_score else high_score
                message1 = f"The second player guessed the number!\nCurrent Score: {score}\nHigh Score: {high_score}\n"
                message2 = f"Congratulations, you have guessed the number!\nCurrent Score: {score}\nHigh Score: {high_score}\n"
                print(f"Game ended. Player finished with a score of {score}.\n")
            elif (guess > number):
                message1 = f"The second player's guess ({guess}) was too high.\n"
                message2 = "Your guess is too high. Try going lower!\n"
            else:
                message1 = f"The second player's guess ({guess}) was too low.\n"
                message2 = "Your guess is too low. Try going higher!\n"

            s1.send(message1.encode())
            s2.send(message2.encode())
        
        play_again = s1.recv(BUFF_SIZE).decode()
        if play_again == 'n':
            playing = False
            s2.send(play_again.encode())
            print("Game ended.")
        elif play_again == FORCE_QUIT:
            s2.send(play_again.encode())
            return FORCE_QUIT


def run_server():
    host = socket.gethostname()
    port = PORT

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(2)
    player_type = "host"

    try:
        print("Awaiting connection...")
        client1_socket, address1 = server_socket.accept()
        print(f"Connection successfully established from address {address1}.\n")
    
        client1_socket.send(player_type.encode())
    
        player_type = "challenger"
        high_score = 0

        while True:
            option = client1_socket.recv(BUFF_SIZE).decode()
            if option == FORCE_QUIT:
                print("Client connection terminated abruptly...")
                break

            if option == PLAY_VS_COMPUTER:
                print("Player vs. Computer starting...")
                score = play_vs_computer(client1_socket, high_score)
                if score == FORCE_QUIT:
                    print("Client connection terminated abruptly...")
                    break
                
                high_score = score if score > high_score else high_score
            elif option == PLAY_VS_PLAYER:
                print("Awaiting connection...")
                client2_socket, address2 = server_socket.accept()
                client2_socket.send(player_type.encode())
                message = "Second player joined the match."
                client1_socket.send(message.encode())
                print(f"Connection successfully established from address {address2}.\n\nPlayer vs. Player starting...")
                result = play_vs_player(client1_socket, client2_socket)

                if result == FORCE_QUIT:
                    print("Client connection terminated abruptly...")
                    break
                elif result == RETURN_TO_MENU:
                    print("Client connection terminated abruptly...")
                    continue
            elif option == EXIT:
                break

        print("Player disconnected.")
        client1_socket.close()
        server_socket.close()
    except:
        try:
            message = FORCE_QUIT
            client1_socket.send(message.encode())
            client2_socket.send(message.encode())
            client1_socket.close()
            client2_socket.close()
        except:
            print("\nThe server encountered an error.\nShutting down...")
            return

        print("\nThe server encountered an error.\nShutting down...")


if __name__ == "__main__":
    run_server()