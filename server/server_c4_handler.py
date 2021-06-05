import random
from server import server_logic, server_c4
from threading import Thread


class C4ServerClass(Thread):
    def __init__(self, client_socket_1, client_socket_2, first_p1):
        Thread.__init__(self)
        self.client_socket_1 = client_socket_1
        self.client_socket_2 = client_socket_2
        self.first_p1 = first_p1

     # Creates the board
        self.board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

        # Set turn yellow/red
        # self.turn = 'red'

        # Store winner/draw
        self.winner = None
        self.draw = None

    def run(self):

        count = 0
        turn = self.first_p1

        if turn == "0":
            print("Sending Turn to player 1")
            server_logic.format_and_send(self.client_socket_1, "turn", "red")
            server_logic.format_and_send(self.client_socket_2, "turn", "yellow")
            turn = "red"
            self.first_p1 = turn
        else:
            print("Sending Turn to player 2")
            server_logic.format_and_send(self.client_socket_2, "turn", "red")
            server_logic.format_and_send(self.client_socket_1, "turn", "yellow")
            turn = "yellow"
            self.first_p1 = turn

        print("In handleServerC4")
        while True:
            if turn == "red":
                data = self.client_socket_1.recv(1024).decode('utf-8')
            else:
                data = self.client_socket_2.recv(1024).decode('utf-8')

            print("Turn = " + str(turn) + ". Data recieced: " + data)
            split = data.split("##")
            print(split[0])

            if split[0] == "move":
                server_c4.set_player_move(split[2], turn, self.board)
                server_logic.format_and_send(self.client_socket_1, "move", split[2])
                server_logic.format_and_send(self.client_socket_2, "move", split[2])

                winner = server_c4.check_game_end(count, turn, self.board)
                count = count + 1

                if winner == "red":
                    if self.first_p1 == "red":
                        self.client_socket_1.send(bytes("Win", 'utf-8'))
                        self.client_socket_2.send(bytes("Lose", 'utf-8'))
                        break
                    else:
                        self.client_socket_2.send(bytes("Win", 'utf-8'))
                        self.client_socket_1.send(bytes("Lose", 'utf-8'))
                        break
                elif winner == "yellow":
                    if self.first_p1 == "yellow":
                        print(self.first_p1)
                        self.client_socket_2.send(bytes("Win", 'utf-8'))
                        self.client_socket_1.send(bytes("Lose", 'utf-8'))
                        break
                    else:
                        self.client_socket_1.send(bytes("Win", 'utf-8'))
                        self.client_socket_2.send(bytes("Lose", 'utf-8'))
                        break
                elif winner == "draw":
                    self.client_socket_1.send(bytes("Draw", 'utf-8'))
                    self.client_socket_2.send(bytes("Draw", 'utf-8'))
                    break

                if turn == "yellow":
                    turn = "red"
                else:
                    turn = "yellow"
