import socket
import random

high_score = 0

def generate_random_number() -> int:
    return random.randint(0, 50)


def play(client: socket):
    return
    # number = generate_random_number()
    # guess = -1
    # score = 5000

    # while guess != number:
    #     guess = int(client.recv().decode())
    #     score -= 100 if score > 0 else 0
    #     high_score = score if score > high_score else high_score
    #     message: str
        
    #     if guess == number:
    #         message = f'''Congratulations, you have guessed the number!
    #         High Score: {high_score}
    #         Current Score: {score}\n'''
    #     elif (guess > number):
    #         message = "Your guess is too high. Try going lower!\n"
    #     else:
    #         message = "Your guess is too low. Try going higher!\n"

    #     client.send(message.encode())

    # return 


def run_server():
    host = socket.gethostname()
    port = 5050

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(2)

    print("Awaiting connection...")
    client_socket, address = server_socket.accept()
    print(f"Connection successfully established from address {address}.")

    while True:
        option = client_socket.recv(4).decode()

        if option == '1':
            play(client_socket)
        elif option == '2':
            play(client_socket)
        elif option == '4':
            break

    print("Player disconnected.")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    run_server()