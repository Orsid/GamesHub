from server import server_db
from server import server_c4_handler
import server


def parse_client_msg(client_message, client_socket):

    client_message = client_message.decode('utf-8')
    split = client_message.split("##")

    message_type = split[0].lower()
    if message_type == "register":
        username = split[1]
        password = split[2]
        email = split[3]
        user_data = (username, password, email)

        server_db.create_user(user_data)
        return username

    if message_type == "login":
        username = split[2]
        password = split[3]

        login_user_data = (username, password)
        valid_user = server_db.validate_user(login_user_data)
        if valid_user == 1:  # user exists
            login_status = 1
        else:
            login_status = -1

        send_login_status(client_socket, login_status)
        return

    if message_type == "game":
        user_list = server.user_list()
        server_socket = server.server_socket()

        other_user = split[1]
        other_socket = user_list[other_user]

        server_c4_handler.run(client_socket, other_socket, server_socket)


def send_login_status(socket, login_status):
    msg = ""
    if login_status == -1:
        msg = "Wrong username or password. Please try again."
    elif login_status == 1:
        msg = "Login successful!"
    send_msg = "login##" + str(login_status) + "##" + msg
    socket.send(bytes(send_msg, 'utf-8'))


