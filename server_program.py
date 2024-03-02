import socket as sk
import json as js
import hashlib


# I used an already existing name on purpose
def hash(password):
    password_bytes = password.encode()
    hash_object = hashlib.sha256()
    hash_object.update(password_bytes)
    return hash_object.hexdigest()


def save_as_file(change, file_name) -> None:
    with open(file_name, "w") as f:
        js.dump(change, f, indent=4)
        # for now there is an indentation for readability, I might change it in the future


def get_from_file(file_name) -> dict:
    with open(file_name, "r") as f:
        content = js.load(f)
    return content


def server_program():
    def log_in_or_sign_up(password_file_name: str, action: str, username: str, password: str) -> bool:
        try:
            passwords = get_from_file(password_file_name)  # dictionary
        except FileNotFoundError:
            passwords = {}
        if action == "LGN":
            if username not in passwords:
                return False
            if passwords[username] == password:
                print("in passwords")
                return True
            else:
                return False

        elif action == "SGN":
            if username in passwords:
                return False
            else:
                passwords.update({username: password})
                save_as_file(passwords, "passwords.txt")
                return True
        else:
            return False

    def change_password(socket: sk.socket, password_file_name: str) -> None:
        passwords = get_from_file(password_file_name)
        info = socket.recv(1024)
        action, change, username = info.decode().split()
        if action != "CHNG":  # CHNG - change
            return None
        passwords.update({change: username})
        save_as_file(passwords, password_file_name)

    host = "localhost"
    port = 5000

    server_socket = sk.socket()
    server_socket.bind((host, port))
    server_socket.listen()
    conn, address = server_socket.accept()
    print("connection from" + str(address))

    while True:
        info = conn.recv(1024)
        action, username, password = info.decode().split()
        permission = log_in_or_sign_up("passwords.txt", action, username, password)  # was access given? T/F
        permission = int(permission)
        conn.send(str(permission).encode())  # send weather access was given

        if permission and action == "LGN":
            change_password(conn, "passwords.txt")
            # I thought of calling this function in log_in_or_sign_up right before returning True in the log in,
            # so I could pass the dictionary instead of the file name, but then I'd need to pass the socket,
            # and for now I don't want to do it

        if conn.recv(128).decode() == "ACK":  # or else it will be CNT - continue
            conn.close()
            break


if __name__ == "__main__":
    server_program()
