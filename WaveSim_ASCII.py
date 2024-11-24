import pygame
import numpy as np

# Setup Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 10
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE
BORDER_MARGIN = 2  # Screen Border

# Pygame Initialization
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("ASCII Wave Sim")

# Define Matrix used to simulate water movement
grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))
new_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))

# Water damuping costant
damping = 0.98

# Font
font = pygame.font.SysFont('monospace', CELL_SIZE)

# Characters used on different water levels
characters = " .:-=+*#%@"

# Mouse tracking variable
prev_mouse_pos = None


#############
# MAIN LOOP #
#############
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            grid_x = mouse_x // CELL_SIZE
            grid_y = mouse_y // CELL_SIZE
            if BORDER_MARGIN <= grid_x < GRID_WIDTH - BORDER_MARGIN and BORDER_MARGIN <= grid_y < GRID_HEIGHT - BORDER_MARGIN:
                grid[grid_y, grid_x] = 400  # Wave strength

    # Mouse movement system
    mouse_pos = pygame.mouse.get_pos()
    if prev_mouse_pos is not None:
        mouse_dx = mouse_pos[0] - prev_mouse_pos[0]
        mouse_dy = mouse_pos[1] - prev_mouse_pos[1]
        velocity = (mouse_dx ** 2 + mouse_dy ** 2) ** 0.5  # Wave Magnitude

        # Waves on mouse movement
        grid_x = mouse_pos[0] // CELL_SIZE
        grid_y = mouse_pos[1] // CELL_SIZE
        if BORDER_MARGIN <= grid_x < GRID_WIDTH - BORDER_MARGIN and BORDER_MARGIN <= grid_y < GRID_HEIGHT - BORDER_MARGIN:
            grid[grid_y, grid_x] += velocity * 4  # Movement strenth amplifier costant

    prev_mouse_pos = mouse_pos

    # Wave propagation
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, GRID_WIDTH - 1):
            new_grid[y, x] = (
                (grid[y - 1, x] +
                 grid[y + 1, x] +
                 grid[y, x - 1] +
                 grid[y, x + 1]) / 2
                - new_grid[y, x]
            )
            new_grid[y, x] *= damping

    grid, new_grid = new_grid, grid  # Swap grids

    # Draw grids
    window.fill((0, 0, 0))  # Background Color!
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            value = grid[y, x]
            index = int((abs(value) / 100) * (len(characters) - 1))
            index = max(0, min(index, len(characters) - 1)) 
            char_surface = font.render(characters[index], True, (0, 255, 255))  # Character Color!
            window.blit(char_surface, (x * CELL_SIZE, y * CELL_SIZE))

    pygame.display.flip()

pygame.quit()

# End