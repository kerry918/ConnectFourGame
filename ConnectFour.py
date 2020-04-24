import numpy as np  # import numpy library to deal with matrices
import pygame
import sys
import math

ROW = 6
COL = 7

BLUE = (0, 0, 255)  # RED, GREEN, BLUE
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


def create_board():
    board = np.zeros((ROW, COL))  # initialized a matrix of 6 by 7 of all zeros
    return board


def drop_piece(board, row, col, piece):  # drop the piece into the board
    board[row][col] = piece  # assign the piece to the location


def is_valid_location(board, col):   # check if the place the player typed in is a valid location
    return board[ROW-1][col] == 0


def get_next_open_row(board, col):  # get the next avaliable open slot for the piece to drop
    for r in range(ROW):
        if board[r][col] == 0:
            return r


def print_board(board):  # change the orientation so what show is the correct position
    print(np.flip(board, 0))  # flip the board


def winning_move(board, piece):   # pass in the board and the last peice that droped
    # Check horizontal locations for win
    for c in range(COL-3):  # -3 is since if the starting position is the last three points, it could not work
        for r in range (ROW):
            # Check if the next four position is equal to the last piece that dropped in
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range (COL):
        for r in range (ROW-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
            # Check if the next four position is equal to the last piece that dropped in

    # Check positively sloped diagonals
    for c in range(COL - 3):
        for r in range(ROW - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
            # Check if the next four position is equal to the last piece that dropped in

    # Check negatively sloped diagonals
    for c in range(COL - 3):
        for r in range(3, ROW - 3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
            # Check if the next four position is equal to the last piece that dropped in

def draw_board(board):
    for c in range(COL):
        for r in range(ROW):
            pygame.draw.rect(screen, BLUE, (c*SQUARE, r*SQUARE+SQUARE, SQUARE, SQUARE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE + SQUARE/2), int(r*SQUARE + 3*SQUARE/2)), RADIUS)

    for c in range(COL):
        for r in range(ROW):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE + SQUARE / 2), height - int(r * SQUARE + SQUARE / 2)),RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE + SQUARE / 2), height - int(r * SQUARE + SQUARE / 2)), RADIUS)

    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARE = 100
width = COL * SQUARE
height = (ROW+1) * SQUARE

size = (width, height)
RADIUS = int(SQUARE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()  # update the screen

font = pygame.font.SysFont("monospace", 60)

while not game_over:  # run the game until the game_over variable is not true
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE))
            posx = event.pos[0]
            if turn == 0:  # player 1
                pygame.draw.circle(screen, RED, (posx, int(SQUARE/2)), RADIUS)
            else:  # player 2
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE / 2)), RADIUS)

        pygame. display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ask for player 1 input
            if turn == 0:  # if the turn equals to zero, player 1's turn
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE)) # round down to the nearest division

                if is_valid_location(board, col):  # first check if this is a valid location
                    row = get_next_open_row(board, col)  # get the new avaliable row open
                    drop_piece(board, row, col, 1)  # drop the peice into the board, 1 is for player one

                    if winning_move(board, 1):
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE))
                        label = font.render("Player 1 wins!!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True

            # Ask for player 2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)  # drop the piece into the board, 2 is for player two

                    if winning_move(board, 2):
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE))
                        label = font.render("Player 2 wins!!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2  # take the remainder, alternate between 0 and 1

            if game_over:
                pygame.time.wait(3000)