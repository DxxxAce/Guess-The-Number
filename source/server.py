import socket
from utils import generate_random_number


def play_vs_computer(s: socket, high_score):
    number = generate_random_number()
    guess = -1
    score = 5100

    while guess != number:
        guess = int(s.recv(4).decode())
        score -= 100 if score > 0 else 0
        message: str
        
        if guess == number:
            high_score = score if score > high_score else high_score

            message = f"Congratulations, you have guessed the number!\nHigh Score: {high_score}\nCurrent Score: {score}\n"
        elif (guess > number):
            message = "Your guess is too high. Try going lower!\n"
        else:
            message = "Your guess is too low. Try going higher!\n"

        s.send(message.encode())

    return high_score


def play_vs_player(s1: socket, s2: socket):
    return


def run_server():
    host = socket.gethostname()
    port = 5050

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(2)

    print("Awaiting connection...")
    client1_socket, address = server_socket.accept()
    print(f"Connection successfully established from address {address}.")

    high_score = 0

    while True:
        option = client1_socket.recv(4).decode()

        if option == '1':
            score = play_vs_computer(client1_socket, high_score)
            high_score = score if score > high_score else high_score
        elif option == '2':
            play_vs_player(client1_socket)
        elif option == '4':
            break

    print("Player disconnected.")
    client1_socket.close()
    server_socket.close()


if __name__ == '__main__':
    run_server()