import os, sys
sys.path.insert(0, os.path.abspath(".."))

from server import server_comm


if __name__ == '__main__':
    server_comm.start_server()

