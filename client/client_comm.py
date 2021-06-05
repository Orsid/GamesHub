import socket
import threading
from threading import Lock
from client import client_logic
import configparser
import client.client_ui

gl_client_socket = None


class ClientThread(threading.Thread):
    client_address = None
    client_socket = None
    clients = []
    lock = Lock()
    user = ""

    def __init__(self, new_client_socket):
        self.client_socket = new_client_socket

        threading.Thread.__init__(self)

    #    def broadcast(self):

    def run(self):
        msg = ''
        while True:
            try:
                data = self.client_socket.recv(2048)
                msg = data.decode('utf-8').lower()
                if msg == 'bye':
                    self.client_socket.close()
            except socket.error as err:
                print("Caught exception socket.error: " + err.strerror)
                self.client_socket.close()
                client.client_ui.show_message_box("Error", "Oops... We lost connection to server. Please restart.")
                self.client_socket.close()
                exit(-1)

            print("from server: ", msg)
            client_logic.process_server_message(msg)


def send_to_server(out_data):
    global gl_client_socket

    gl_client_socket.sendall(bytes(out_data, 'UTF-8'))


def start_client_comm():
    global gl_client_socket

    server_address_result = get_server_ip()

    try:
        gl_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gl_client_socket.connect((server_address_result[0], int(server_address_result[1])))
    except socket.error as err:
        client.client_ui.show_message_box("Error", "Oops... Unable to connect to server... \n\nError: " + err.strerror)
        exit(-1)

    new_thread = ClientThread(gl_client_socket)
    new_thread.start()


def get_server_ip():
    server_ip = server_port = ""

    try:
        config = configparser.ConfigParser()
        config.read('../config.ini')

        server_ip = config.get('NETWORK', 'server_ip')
        server_port = config.get('NETWORK', 'server_port')
    except configparser.NoSectionError or configparser.NoOptionError:
        client.client_ui.show_message_box("GamesHub - Error", "Error reading config.ini file. \n\nPlease check the "
                                                              "documentation for details.")
        exit(0)

    if server_ip == '' or server_port == '':
        client.client_ui.show_message_box("GamesHub - Error", "Server IP and Port are not configured. \n\nPlease "
                                                              "check the documentation for details.")
        exit(0)

    return server_ip, server_port
