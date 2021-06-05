import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from client import client_comm, client_ui

if __name__ == '__main__':
    # connect to the server
    client_comm.start_client_comm()

    # open the login UI
    client_ui.open_login_ui()

