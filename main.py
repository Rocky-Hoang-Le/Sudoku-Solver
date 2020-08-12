# Sudoku Solver project
# Goal of this project is to make a script that will solve a sudoku puzzle.
# 1. Draw Pygame Screen and grid
# 2. Ability to populate the squares
# 3. Allow user to interact with each cell and place a number and update the grid
# 4. Start creating the solver for the sudoku using back tracking

# Import required modules
import pygame

pygame.init()  # Initialize pygame stuff

# Constants
FPS_CLOCK = pygame.time.Clock()  # Setup Fps timer
FPS = 15  # Set Fps
SCREEN_SIZE_MULTIPLIER = 5  # Since the game is grid based the screen size needs to maintain a certain ratio
SCREEN_SIZE = 81
SQUARE_SIZE = int((SCREEN_SIZE * SCREEN_SIZE_MULTIPLIER) / 3)  # Size of the 3x3 squares
CELL_SIZE = int(SQUARE_SIZE / 3)  # Size of the cells inside the 3 x 3 grids
NUMBER_SIZE = int(CELL_SIZE / 3)  # Size of the small note numbers
SCREEN_WIDTH = SCREEN_SIZE * SCREEN_SIZE_MULTIPLIER
SCREEN_HEIGHT = SCREEN_SIZE * SCREEN_SIZE_MULTIPLIER

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sudoku Solver')

# Font information
font_size = 40
font = pygame.font.Font('freesansbold.ttf', font_size)

# Mouse information
mouse_clicked = False
mouse_x = 0
mouse_y = 0

# Color constants for drawing grid and numbers
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)


# This function will draw the 9 x 9 grid
def draw_grid():
    # Draw small 3x3 cells
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):  # draw vertical lines
        pygame.draw.line(window, LIGHT_GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):  # draw horizontal lines
        pygame.draw.line(window, LIGHT_GRAY, (0, y), (SCREEN_WIDTH, y))

    # Draw the large 3x3 cell
    for x in range(0, SCREEN_WIDTH, SQUARE_SIZE):  # draw vertical lines
        pygame.draw.line(window, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, SQUARE_SIZE):  # draw horizontal lines
        pygame.draw.line(window, BLACK, (0, y), (SCREEN_WIDTH, y))

    return None


initial_grid = [0 for x in range(81)]  # Fill each grid cell with 0s


# Creates the initial sudoku grid
def initialize_cells(grid):
    sudoku_grid = {}
    for y in range(0, 9):
        for x in range(0, 9):
            sudoku_grid[x, y] = grid.pop(0)
    return sudoku_grid


# This functions sets the cell to the number
def set_cell(cell_number, x, y):
    cell = font.render(str(cell_number), True, BLACK)
    cell_rect = cell.get_rect()
    cell_rect.topleft = (x, y)
    window.blit(cell, cell_rect)


# This function displays the number if applicable in each cell
def display_cells(grid):
    for position in grid:
        cell_number = grid[position]
        if cell_number != 0:
            set_cell(cell_number, (position[0] * CELL_SIZE) + 9, (position[1] * CELL_SIZE) + 7)
    return None


# This function returns the picked cell position based on mouse coord
def pick_cell(x, y):
    def check_cell(mouse_coord):
        cell_num = 0
        for cell in range(CELL_SIZE, SCREEN_WIDTH, CELL_SIZE):
            if mouse_coord <= cell:
                return cell_num
            else:
                cell_num += 1
        return 8

    x_cell = check_cell(x)
    y_cell = check_cell(y)
    return x_cell, y_cell


# This function changes the cell number based on number passed
def change_cell(x, y, grid, number, position=None):
    if position is None:
        position = pick_cell(x, y)
    grid[position] = number


# This function checks if a number can be placed legally on the grid
def check_grid(grid, column, row, num):
    # Sub function to check if row contains the same num to place
    def check_row():
        for x in range(0, 9):
            if grid[(x, row)] == num:
                return True
        return False

    # Sub function to check if column contains the same num to place
    def check_column():
        for y in range(0, 9):
            if grid[(column, y)] == num:
                return True
        return False

    # Sub functions to check if the 3x3 contains the same num to place
    # Sub function to check which 3x3 to test
    def box_location():
        if row in range(0, 3):
            box_x = [0, 1, 2]
            if column in range(0, 3):
                box_y = [0, 1, 2]
            elif column in range(3, 6):
                box_y = [3, 4, 5]
            elif column in range(6, 9):
                box_y = [6, 7, 8]
        if row in range(3, 6):
            box_x = [3, 4, 5]
            if column in range(0, 3):
                box_y = [0, 1, 2]
            elif column in range(3, 6):
                box_y = [3, 4, 5]
            elif column in range(6, 9):
                box_y = [6, 7, 8]
        if row in range(6, 9):
            box_x = [6, 7, 8]
            if column in range(0, 3):
                box_y = [0, 1, 2]
            elif column in range(3, 6):
                box_y = [3, 4, 5]
            elif column in range(6, 9):
                box_y = [6, 7, 8]
        return box_x, box_y

    # Sub function check if the 3x3 contains the number
    def check_box():
        for y in box_location()[0]:
            for x in box_location()[1]:
                if grid[(x, y)] == num:
                    return True
        return False

    return not check_box() and not check_row() and not check_column()


# This function will return an unsigned cell position
def find_empty_cell(grid, pos):
    for y in range(0, 9):
        for x in range(0, 9):
            if grid[(x, y)] == 0:
                pos[0] = y
                pos[1] = x
                return True
    return False


# This function uses backtracking to solve the sudoku
def solve_sudoku(grid):
    # Assign row and col an empty position on the grid
    pos = [0, 0]
    if not find_empty_cell(grid, pos):
        return True
    row = pos[0]
    col = pos[1]

    # Start recursion of this function to solve sudoku
    for num in range(1, 10):
        if check_grid(grid, col, row, num):
            change_cell(0, 0, grid, num, (col, row))
            if solve_sudoku(grid):
                return True
            grid[(col, row)] = 0
    # If this is reached we have backtracked
    return False


current_grid = initialize_cells(initial_grid)
display_cells(current_grid)
solve = False  # Check to see if the sudoku should be auto-solved
run = True
while run:  # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEMOTION:  # Checks mouse movement
            mouse_x, mouse_y = event.pos
            mouse_clicked = False

        elif event.type == pygame.MOUSEBUTTONUP:  # Checks mouse clicks
            mouse_x, mouse_y = event.pos
            mouse_clicked = True

    # Draw the game
    window.fill(WHITE)
    display_cells(current_grid)
    draw_grid()
    if solve:
        mouse_clicked = False
        if solve_sudoku(current_grid):
            print('Success')
        else:
            print('Invalid grid')

    # Main game, if cell is clicked change cell number based on input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        solve = True
    if mouse_clicked:
        if keys[pygame.K_1]:
            change_cell(mouse_x, mouse_y, current_grid, 1)
            mouse_clicked = False
        if keys[pygame.K_2]:
            change_cell(mouse_x, mouse_y, current_grid, 2)
            mouse_clicked = False
        if keys[pygame.K_3]:
            change_cell(mouse_x, mouse_y, current_grid, 3)
            mouse_clicked = False
        if keys[pygame.K_4]:
            change_cell(mouse_x, mouse_y, current_grid, 4)
            mouse_clicked = False
        if keys[pygame.K_5]:
            change_cell(mouse_x, mouse_y, current_grid, 5)
            mouse_clicked = False
        if keys[pygame.K_6]:
            change_cell(mouse_x, mouse_y, current_grid, 6)
            mouse_clicked = False
        if keys[pygame.K_7]:
            change_cell(mouse_x, mouse_y, current_grid, 7)
            mouse_clicked = False
        if keys[pygame.K_8]:
            change_cell(mouse_x, mouse_y, current_grid, 8)
            mouse_clicked = False
        if keys[pygame.K_9]:
            change_cell(mouse_x, mouse_y, current_grid, 9)
            mouse_clicked = False

    pygame.display.update()
    FPS_CLOCK.tick(FPS)

pygame.display.quit()
pygame.quit()
