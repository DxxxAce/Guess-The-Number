import socket
from utils import generate_random_number


def play_vs_computer(s: socket, high_score) -> int:
    number = generate_random_number()
    guess = -1
    score = 5100

    while guess != number:
        guess = int(s.recv(4).decode())
        score -= 100 if score > 0 else 0
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
        number = int(s1.recv(1024).decode())
        guess = -1
        score = 5100

        message = "The host is done picking."
        s2.send(message.encode())

        while guess != number:
            guess = int(s2.recv(4).decode())
            score -= 100 if score > 0 else 0
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
        
        play_again = s1.recv(4).decode()
        if play_again == 'n':
            playing = False
            s2.send(play_again.encode())
            print("Game ended.")


def run_server():
    host = socket.gethostname()
    port = 5050

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(2)
    player_type = "host"

    print("Awaiting connection...")
    client1_socket, address1 = server_socket.accept()
    print(f"Connection successfully established from address {address1}.\n")
    client1_socket.send(player_type.encode())

    player_type = "challenger"
    high_score = 0

    while True:
        option = client1_socket.recv(4).decode()

        if option == '1':
            print("Player vs. Computer starting...")
            score = play_vs_computer(client1_socket, high_score)
            high_score = score if score > high_score else high_score
        elif option == '2':
            print("Awaiting connection...")
            client2_socket, address2 = server_socket.accept()
            client2_socket.send(player_type.encode())
            message = "Second player joined the match."
            client1_socket.send(message.encode())
            print(f"Connection successfully established from address {address2}.\n\nPlayer vs. Player starting...")
            play_vs_player(client1_socket, client2_socket)
        elif option == '4':
            break

    print("Player disconnected.")
    client1_socket.close()
    server_socket.close()


if __name__ == '__main__':
    run_server()