import pygame
from minesweeper_logic import initMap, reveal, game_lost, check_win, place_flag
import sys

# Initialize pygame
pygame.init()

# Game variables
map, revealed = initMap(18, 16, 40)

# Set up display
screen_width = len(revealed[0]) * 40
screen_height = len(revealed) * 40
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Define font
font = pygame.font.Font(None, 36)
#Create Button class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, surface):
        #pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(screen, GRAY, self.rect, 2)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

# Function to draw the grid
def draw_grid(revealed):
    for row in range(len(revealed)):
        for col in range(len(revealed[0])):
            cell = revealed[row][col]
            color = WHITE
            border_color = GRAY
            pygame.draw.rect(screen, color, (col * 40, row * 40, 40, 40))
            pygame.draw.rect(screen, border_color, (col * 40, row * 40, 40, 40), 2)
            
            if isinstance(cell, int):
                text = font.render(str(cell), True, BLACK)
                text_rect = text.get_rect(center=(col * 40 + 25, row * 40 + 25))
                screen.blit(text, text_rect)
            if cell=="f":
                text = font.render(str(cell), True, RED)
                text_rect = text.get_rect(center=(col * 40 + 25, row * 40 + 25))
                screen.blit(text, text_rect)

def play_again():
    map, revealed = initMap(18, 16, 40)
    run(map, revealed)


def quit_game():
    print("User chose to quit.")
    pygame.quit()
    sys.exit()

def show_play_again_prompt(revealed):
    play_again_button = Button("Play Again", screen_width // 2 - 100, screen_height // 2 - 25, 200, 50, WHITE, BLACK, play_again)
    quit_button = Button("Quit", screen_width // 2 - 100, screen_height // 2 + 50, 200, 50, WHITE, BLACK, quit_game)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            play_again_button.handle_event(event)
            quit_button.handle_event(event)

        draw_grid(revealed)
        play_again_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()


def run(map, revealed):
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.key.get_mods() & pygame.KMOD_CTRL:  # Ctrl + Left mouse button
                mouse_x, mouse_y = event.pos
                clicked_row = mouse_y // 40
                clicked_col = mouse_x // 40
                place_flag(map, revealed, clicked_row, clicked_col)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                clicked_row = mouse_y // 40
                clicked_col = mouse_x // 40
                revealed = reveal(map, revealed, clicked_row, clicked_col)
            
            

        screen.fill((0, 0, 0))
        draw_grid(revealed)
        if (game_lost(map, revealed)):
            show_play_again_prompt(revealed)
        if (check_win(map, revealed)):
            show_play_again_prompt(revealed)
        pygame.display.flip()

    pygame.quit()

run(map, revealed)