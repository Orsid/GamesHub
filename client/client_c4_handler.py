from threading import Thread
from client import client_logic, client_c4, client_ui, client_comm


class LaunchC4(Thread):

    def __init__(self, first_turn):
        Thread.__init__(self)

        self.myTurn = str(first_turn)
        if self.myTurn == "0":
            self.myTurn = "red"
        if self.myTurn == "1":
            self.myTurn = "yellow"

    def run(self):
        client_c4.start_pg()
        print(self.myTurn)
        client_c4.game_initiating_window()

        msg = "startGame"
        client_logic.formats_server_msg(msg, "")

        while True:
            move = client_c4.check_client_activity()
            move = str(move)
            print("sending move: " + move)
            client_logic.formats_server_msg("move", move)


def start_client_comm_thread():
    print("Starting a new game")
    new_board = LaunchC4(1)
    new_board.start()


def process_c4_server_message(serv_resp):
    msg = ""

    split = serv_resp.split("##")
    split[0] = split[0].lower()

    if split[0] == "move":
        client_c4.draw_board(split[1])
        return
    elif split[0] == "win":
        msg = "You win!!!"
        client_c4.end_game(split[0])
    elif split[0] == "lose":
        msg = "You lost :("
        client_c4.end_game(split[0])
    elif split[0] == "draw":
        msg = "It's a draw!"
        client_c4.end_game(split[0])

    if client_ui.show_yes_no_message_box("Game Ended", msg + "\n\nDo you want to play again?") == "yes":
        print("restarting game")
        client_comm.start_client_comm()
        start_client_comm_thread()
