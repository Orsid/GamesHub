from client import client_comm, client_ui, client_c4_handler, client_c4

clientId = "1"


# outgoing messages
def formats_server_msg(operation, operation_data):
    # format the needed extra information
    # Operation, Username, Game, Message
    global clientId
    out_str = operation + "##" + clientId + "##" + operation_data
    client_comm.send_to_server(out_str)
    print("Sent to server: " + out_str)
    return out_str


def bl_login(out_str):
    formats_server_msg("login", out_str)


def bl_signup(out_str):
    formats_server_msg("signup", out_str)


# incoming messages
def process_server_message(msg):
    split = msg.split("##")
    message_type = split[0].lower()

    if message_type == "login":
        return_code = split[1]
        return_msg = split[2]
        if return_code == '1':
            client_ui.close_login_ui()
            client_c4_handler.start_client_comm_thread()
        else:
            client_ui.show_login_msg_info(return_msg)

    elif message_type == "signup":
        return_code = split[1]
        return_msg = split[2]
        if return_code == '1':
            client_ui.close_signup_ui()
        else:
            client_ui.show_signup_msg_info(return_msg)

    elif message_type == "inqueue":
        client_c4.set_message("Waiting for second player to connect...")
        return

    elif message_type == "move" or message_type == "win" or message_type == "lose" or message_type == "draw":
        client_c4_handler.process_c4_server_message(msg)

    elif message_type == "turn":
        client_c4.set_turn(split[1])
