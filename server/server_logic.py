from server import server_db, server_comm, server_c4_handler
import random
import time


def parse_client_msg(client_socket, client_message):
    split = client_message.split("##")
    message_type = split[0].lower()

    if message_type == "signup":
        first_name = split[2]
        last_name = split[3]
        username = split[4]
        email = split[5]
        password = split[6]
        user_data = (first_name, last_name, username, password, email)

        valid_user = server_db.create_user(user_data)
        if valid_user == -1:  # userName exists
            signup_status = -1
        else:
            signup_status = 1

        send_signup_status(client_socket, signup_status)
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

    if message_type == "startgame":
        wait_for_game(client_socket)


def send_login_status(socket, login_status):
    msg = ""
    if login_status == -1:
        msg = "-1##Wrong username or password. Please try again."
    elif login_status == 1:
        msg = "1##Login successful!"

    format_and_send(socket, "login", msg)


#    sendMsg = "login##" + str(loginStatus) + "##" + msg
#    server_comm.sendToClient(socket, sendMsg)

def send_signup_status(socket, signup_status):
    msg = ""
    if signup_status == -1:
        msg = "-1##Username already exists. Please try again."
    elif signup_status == 1:
        msg = "1##Signup successful!"

    format_and_send(socket, "signup", msg)


def format_and_send(socket, command, message):
    msg = command + "##" + message
    print("Sent to client: " + msg)
    server_comm.send_to_client(socket, msg)


def wait_for_game(client_socket):
    wait_list = server_comm.get_wait_list()

    if len(wait_list) > 0:

        first_user = wait_list[0]

        # Randomizes first player
        first_p1 = str(random.randint(0, 1))

        new_thread = server_c4_handler.C4ServerClass(first_user, client_socket, first_p1)
        new_thread.start()

        time.sleep(3)

        if first_p1 == "1":
            format_and_send(first_user, "startgame", "0")
            format_and_send(client_socket, "startgame", "1")
        else:
            format_and_send(first_user, "startgame", "1")
            format_and_send(client_socket, "startgame", "0")

        # Resets the list of currently waiting users
        server_comm.clear_wait_list()

    else:
        wait_list.append(client_socket)
        format_and_send(client_socket, "inQueue", "You have been added to the queue")
