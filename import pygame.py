import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 300
screen_height = 600
block_size = 30

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
purple = (128, 0, 128)
orange = (255, 165, 0)

# Shape formats
shapes = {
    'S': [['.....',
           '.....',
           '..00.',
           '.00..',
           '.....'],
          ['.....',
           '..0..',
           '..00.',
           '...0.',
           '.....']],
    'Z': [['.....',
           '.....',
           '.00..',
           '..00.',
           '.....'],
          ['.....',
           '..0..',
           '.00..',
           '.0...',
           '.....']],
    'I': [['.....',
           '.....',
           '0000.',
           '.....',
           '.....'],
          ['..0..',
           '..0..',
           '..0..',
           '..0..',
           '.....']],
    'O': [['.....',
           '.....',
           '.00..',
           '.00..',
           '.....']],
    'J': [['.....',
           '.0...',
           '.000.',
           '.....',
           '.....'],
          ['.....',
           '..00.',
           '..0..',
           '..0..',
           '.....'],
          ['.....',
           '.....',
           '.000.',
           '...0.',
           '.....'],
          ['.....',
           '..0..',
           '..0..',
           '.00..',
           '.....']],
    'L': [['.....',
           '...0.',
           '.000.',
           '.....',
           '.....'],
          ['.....',
           '..0..',
           '..0..',
           '..00.',
           '.....'],
          ['.....',
           '.....',
           '.000.',
           '.0...',
           '.....'],
          ['.....',
           '.00..',
           '..0..',
           '..0..',
           '.....']],
    'T': [['.....',
           '..0..',
           '.000.',
           '.....',
           '.....'],
          ['.....',
           '..0..',
           '..00.',
           '..0..',
           '.....'],
          ['.....',
           '.....',
           '.000.',
           '..0..',
           '.....'],
          ['.....',
           '..0..',
           '.00..',
           '..0..',
           '.....']]
}

# Corresponding shape colors
shape_colors = {
    'S': green,
    'Z': red,
    'I': cyan,
    'O': yellow,
    'J': blue,
    'L': orange,
    'T': purple
}

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

def create_grid(locked_positions={}):
    grid = [[black for _ in range(screen_width // block_size)] for _ in range(screen_height // block_size)]
    for (x, y), color in locked_positions.items():
        grid[y][x] = color
    return grid

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (x * block_size, y * block_size, block_size, block_size), 0)
    draw_gridlines(surface)

def draw_gridlines(surface):
    for x in range(screen_width // block_size):
        pygame.draw.line(surface, white, (x * block_size, 0), (x * block_size, screen_height))
    for y in range(screen_height // block_size):
        pygame.draw.line(surface, white, (0, y * block_size), (screen_width, y * block_size))

def draw_window(surface, grid):
    surface.fill(black)
    draw_grid(surface, grid)
    pygame.display.update()

def get_shape():
    shape = random.choice(list(shapes.keys()))
    return shapes[shape], shape_colors[shape]

def convert_shape_format(shape, rotation, x_offset=0, y_offset=0):
    positions = []
    shape_format = shape[rotation % len(shape)]
    for y, line in enumerate(shape_format):
        for x, char in enumerate(line):
            if char == '0':
                positions.append((x + x_offset, y + y_offset))
    return positions

def check_collision(shape_positions, grid):
    for x, y in shape_positions:
        if x < 0 or x >= screen_width // block_size or y >= screen_height // block_size or grid[y][x] != black:
            return True
    return False

def lock_positions(shape_positions, color, locked_positions):
    for x, y in shape_positions:
        locked_positions[(x, y)] = color

def clear_rows(grid, locked_positions):
    cleared = 0
    for y in range(len(grid) - 1, -1, -1):
        row = grid[y]
        if black not in row:
            cleared += 1
            del_row(y, grid, locked_positions)
    return cleared

def del_row(row, grid, locked_positions):
    for x in range(len(grid[row])):
        try:
            del locked_positions[(x, row)]
        except:
            continue
    for y in range(row, 0, -1):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                locked_positions[(x, y + 1)] = locked_positions.pop((x, y))

def rotate_shape(shape, rotation):
    return (rotation + 1) % len(shape)

def move_shape(shape_positions, dx, dy):
    return [(x + dx, y + dy) for x, y in shape_positions]

def valid_space(shape_positions, grid):
    for x, y in shape_positions:
        if x < 0 or x >= screen_width // block_size or y >= screen_height // block_size or grid[y][x] != black:
            return False
    return True

def check_lost(locked_positions):
    for (x, y) in locked_positions:
        if y < 1:
            return True
    return False

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    
    current_piece, color = get_shape()
    current_rotation = 0
    current_positions = convert_shape_format(current_piece, current_rotation, 5, 0)

    change_piece = False
    run = True
    fall_time = 0
    fall_speed = 0.3

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            new_positions = move_shape(current_positions, 0, 1)
            if not valid_space(new_positions, grid):
                lock_positions(current_positions, color, locked_positions)
                current_piece, color = get_shape()
                current_rotation = 0
                current_positions = convert_shape_format(current_piece, current_rotation, 5, 0)
                if not valid_space(current_positions, grid):
                    run = False
                    print("You Lost")
            else:
                current_positions = new_positions

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_positions = move_shape(current_positions, -1, 0)
                    if valid_space(new_positions, grid):
                        current_positions = new_positions

                elif event.key == pygame.K_RIGHT:
                    new_positions = move_shape(current_positions, 1, 0)
                    if valid_space(new_positions, grid):
                        current_positions = new_positions

                elif event.key == pygame.K_DOWN:
                    new_positions = move_shape(current_positions, 0, 1)
                    if valid_space(new_positions, grid):
                        current_positions = new_positions

                elif event.key == pygame.K_UP:
                    new_rotation = rotate_shape(current_piece, current_rotation)
                    new_positions = convert_shape_format(current_piece, new_rotation, current_positions[0][0], current_positions[0][1])
                    if valid_space(new_positions, grid):
                        current_rotation = new_rotation
                        current_positions = new_positions

        grid = create_grid(locked_positions)
        for pos in current_positions:
            x, y = pos
            grid[y][x] = color

        clear_rows(grid, locked_positions)
        draw_window(screen, grid)

    pygame.quit()

if __name__ == "__main__":
    main()
