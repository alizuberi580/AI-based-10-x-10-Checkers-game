import pygame
from checkers.game import Game
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.board import Board
from checkers.piece import Piece
from minimax.algorithm import minimax
pygame.init()          # Initialize all pygame modules
pygame.font.init()     # Initialize the font module
#now reason why we cant import using checkes directly is that in checkers folder we included the file __init__.py 
#which tells the main file that checkers directory is now a package folder and that things can be imported from it directly

# FPS (Frames Per Second) setting
FPS = 60

# Initialize the game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# Function to get the row and column from mouse click position
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Function to display the winner and restart option
def draw_end_screen(winner):
    WIN.fill((0, 0, 0))  # Clear the screen
    font = pygame.font.SysFont('arial', 48)
    text = font.render(f"{winner} Wins!", True, (255, 255, 255))
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))

    restart_text = font.render("Click to Restart", True, (255, 255, 255))
    WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()

# Main game loop function
def main():
    run = True
    clock = pygame.time.Clock()  # Clock to control FPS
    game = Game(WIN)
    winner = None

    while run:
        clock.tick(FPS)  # Control the frame rate

        if winner:  # Display winner screen if game ends
            draw_end_screen(winner)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main()  # Restart the game

        else:
            if game.turn == WHITE:  # AI's turn (White)
                value, new_board = minimax(game.get_board(), 5, WHITE, game)
                game.ai_move(new_board)

            if game.winner() is not None:  # Check for a winner
                w= game.winner()
                if w==RED:
                    winner='RED'
                else:
                    winner='WHITE'
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:  # Player's move (Red)
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    if game.turn == RED:
                        game.select(row, col)

            game.update()

    pygame.quit()

# Start the game
main()
