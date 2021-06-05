import pygame as pg
import os
from pygame.locals import *

# Creates the board
board = None
screen = None

# Set turn by color (yellow/red)
turn = 'yellow'
msg = 'Waiting for second player to join...'
assigned = False
init = True

# Store winner/draw
winner = False
loser = False
draw = False

# Size of board in pixels
width = 630
height = 630

# Background color, divider lines
white = (255, 255, 255)
line_color = (0, 0, 0)

# Set images that will be used
initiating_window = pg.image.load("../res/c4_cover.png")
red_img = pg.image.load("../res/c4_red_piece.png")
yellow_img = pg.image.load("../res/c4_yellow_piece.png")

# Scales the image to the size of the board
initiating_window = pg.transform.scale(initiating_window, (width, height + 100))
red_img = pg.transform.scale(red_img, (50, 50))
yellow_img = pg.transform.scale(yellow_img, (50, 50))


def start_pg():
    global screen, init, board

    board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

    if init:
        # Starting up pygame
        pg.init()

        # Track time (future...)
        pg.time.Clock()

        # Set display
        screen = pg.display.set_mode((width, height + 100), 0, 32)
        pg.display.set_caption("Connect Four")

        init = False

    else:
        global turn, msg, assigned, winner, loser, draw
        # Set turn by color (yellow/red)
        turn = 'yellow'
        msg = 'Waiting for second player to join...'
        assigned = False

        # Store winner/draw
        winner = False
        loser = False
        draw = False


def game_initiating_window():
    global screen

    # Puts the cover image over the screen
    screen.fill(white)

    # draws the board
    # drawing vertical lines:
    for i in range(1, 7):
        pg.draw.line(screen, line_color, (width / 7 * i, 0), (width / 7 * i, height), 7)

    # drawing horizontal lines
    for i in range(1, 6):
        pg.draw.line(screen, line_color, (0, height / 6 * i), (width, height / 6 * i), 7)
    draw_status()
    pg.display.update()


def draw_status():
    global draw, turn, msg, assigned, screen

    if assigned:
        if not winner and not draw and not loser:
            if turn == 'yellow':
                message = "It is player's 2 turn"
            else:
                message = "It is now your turn"
            assigned = True
        elif draw is True:
            message = "The game ended in a draw!"
            assigned = True
        elif winner:
            message = "You have won!!!!"
            assigned = True
        else:
            message = "Sadly you've lost, better luck next time!"
            assigned = True
    else:
        message = msg
        assigned = True

    # setting a font object
    font = pg.font.Font(None, 30)

    # setting the font properties
    text = font.render(message, True, (255, 255, 255))

    # copy the rendered message onto the board, creating a small block at the bottom of the main display
    screen.fill((0, 0, 0), (0, 630, 630, 100))
    text_rect = text.get_rect(center=(width / 2, 680))
    screen.blit(text, text_rect)


#    pg.display.update()


def draw_board(col):
    global board, turn, screen

    check = check_empty_tile(col)
    row = check[1]

    col = int(col)
    col = col - 1

    posx = (col * 90) + 20

    posy = 540 - (row * 107) + 20

    if turn == "red":
        screen.blit(red_img, (posx, posy))
    else:
        screen.blit(yellow_img, (posx, posy))

    print("Printing in x,y = " + str(posx), ", " + str(posy))
    set_player_move(col, row)

    draw_status()
    pg.display.update()


def get_player_move():
    x, y = pg.mouse.get_pos()

    for i in range(1, 8):
        if x < width / 7 * i:
            x = i
            break
    check = check_empty_tile(x)
    print("printing check[0]")
    print(check[0])
    if check[0] is True:
        return x
    else:
        return None


def check_empty_tile(move):
    move = int(move)

    for x in range(len(board)):
        if board[x][move - 1] == ' ':
            print(x)
            print(move - 1)
            return True, x
    return False, None


def set_player_move(col, row):
    global turn

    col = int(col)
    row = int(row)

    board[row][col] = turn

    if turn == "red":
        turn = "yellow"
    else:
        turn = "red"


def check_client_activity():
    global turn, winner, draw
    move = None

    while True:
        done = False

        while True:
            if not done:
                for event in pg.event.get():
                    if event.type == QUIT:
                        pg.quit()
                        os._exit(0)
                    elif event.type == MOUSEBUTTONDOWN:
                        print("got Turn mouse event. Turn is: " + str(turn))
                        if turn != "red":
                            continue
                        move = get_player_move()
                        if move is not None:
                            print("Move is: " + str(move))
                            return move
                        else:
                            print("Invalid Move. Column is full")
            elif done:
                if pg.event.get(eventtype=QUIT):
                    pg.quit()
                    os._exit(0)
            elif move is not None:
                return move


def end_game(status):
    global winner, loser, draw, turn
    if status == "win":
        winner = True
        turn = None
        draw_status()
        pg.display.update()

    elif status == "lose":
        loser = True
        turn = None
        draw_status()
        pg.display.update()

    elif status == "draw":
        draw = True
        turn = None
        draw_status()
        pg.display.update()


def get_turn():
    global turn
    return turn


def set_turn(current_turn):
    global turn
    print("Client's turn is set to: " + current_turn)
    turn = current_turn

    # show on screen that the game started
    draw_status()
    pg.display.update()


def set_message(current_message):
    global msg
    msg = current_message
