import pygame
from minesweeper_logic import initMap, reveal, game_lost, check_win

# Initialize pygame
pygame.init()

# Game variables
map, revealed = initMap(4, 4, 1)

# Set up display
screen_width = len(revealed[0]) * 50
screen_height = len(revealed) * 50
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Define font
font = pygame.font.Font(None, 36)

# Function to draw the grid
def draw_grid(revealed):
    for row in range(len(revealed)):
        for col in range(len(revealed[0])):
            cell = revealed[row][col]
            color = WHITE
            border_color = GRAY
            if cell == "_":
                pygame.draw.rect(screen, color, (col * 50, row * 50, 50, 50))
            else:
                pygame.draw.rect(screen, color, (col * 50, row * 50, 50, 50))
                pygame.draw.rect(screen, border_color, (col * 50, row * 50, 50, 50), 2)
                if isinstance(cell, int):
                    text = font.render(str(cell), True, BLACK)
                    text_rect = text.get_rect(center=(col * 50 + 25, row * 50 + 25))
                    screen.blit(text, text_rect)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_x, mouse_y = event.pos
            clicked_row = mouse_y // 50
            clicked_col = mouse_x // 50
            revealed = reveal(map, revealed, clicked_row, clicked_col)

    screen.fill((0, 0, 0))
    draw_grid(revealed)
    if (game_lost(map, revealed)):
        running = False;
    if (check_win(map, revealed)):
        running = False;
    pygame.display.flip()

pygame.quit()
