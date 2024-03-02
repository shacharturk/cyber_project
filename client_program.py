import socket as sk
import hashlib


def hash(password):
    password_bytes = password.encode()
    hash_object = hashlib.sha256()
    hash_object.update(password_bytes)
    return hash_object.hexdigest()


def client_program():
    def log_in_or_sign_up(socket, act):
        while True:
            username = input("please enter your user name: ")
            password = input("please enter your password: ")
            password = hash(password)
            socket.send(f"{act} {username} {password}".encode())  # hash(password)
            if int(socket.recv(32).decode()):
                if act == "LGN":
                    change_password(socket, username)
                return True
            else:
                if act == "LGN":
                    print("invalid password or user name, please try again")
                elif act == "SGN":
                    print("user name is already taken, please enter a different one")
                else:
                    raise "invalid action. valid actions are only LGN, SGN (at the moment)"
            socket.send("CNT".encode())  # CNT - continue (sent instead of the ACK - acknowledge that is sent in the end

    def change_password(socket, username) -> None:
        change = input("would you like to change your password? (yes/no)\n")
        if change != "yes":
            socket.send(f"NO NO NO".encode())
            return None
        pass1 = input("please enter an alternate password:\n")
        pass2 = input("please enter it again for validation:\n")
        if pass1 == pass2:
            action = "CHNG"  # change
        else:
            action = ""
        socket.send(f"{action} {username} {hash(pass1)}".encode())  # change

    def execute_connection(socket) -> None:
        action = input("Would you like to sign up or log in? ")

        if action == "log in":
            if int(log_in_or_sign_up(socket, "LGN")):  # bool
                print("you're logged in")
                # enter_account()

            else:
                print("password or username are not valid")

        elif action == "sign up":
            if log_in_or_sign_up(socket, "SGN"):  # bool
                # enter_account()
                print("your account has been created. you're in")
            else:
                print("username already exists. please (exit and) try again")

        else:
            print("invalid action")
            execute_connection(socket)

    host = "localhost"
    port = 5000

    client_socket = sk.socket()
    client_socket.connect((host, port))

    execute_connection(client_socket)
    client_socket.send("ACK".encode())
    client_socket.close()


if __name__ == "__main__":
    client_program()
