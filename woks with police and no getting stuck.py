import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 850, 800
block_size = 20

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DRIVERR")

# Maze
maze = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "     #.##### ## #####.#     ",
    "     #.##          ##.#     ",
    "######.##          ##.######",
    ".......##          ##.......",
    "######.##          ##.######",
    "     #.##          ##.#     ",
    "     #.##          ##.#     ",
    "######.##############.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#o..##................##..o#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Load car image
racecar_image = pygame.image.load("car.png")
racecar_image = pygame.transform.scale(racecar_image, (block_size, block_size))

# Load ghost image
ghost_image = pygame.image.load("ghost.png")
ghost_image = pygame.transform.scale(ghost_image, (block_size, block_size))

# Function to draw the maze
def draw_maze(screen, maze):
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == "#":
                pygame.draw.rect(screen, BLUE, (x * block_size, y * block_size, block_size, block_size))
            elif char == ".":
                pygame.draw.circle(screen, WHITE, (x * block_size + block_size // 2, y * block_size + block_size // 2), 3)
            elif char == "o":
                pygame.draw.circle(screen, WHITE, (x * block_size + block_size // 2, y * block_size + block_size // 2), 8)

# Function to draw the car
def draw_racecar(screen, x, y):
    screen.blit(racecar_image, (x * block_size, y * block_size))

# Ghost class
class Ghost:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, block_size, block_size)

    def move_towards(self, target_x, target_y):
        if self.rect.x < target_x * block_size:
            self.rect.x += 0.5  # Ghost speed
        elif self.rect.x > target_x * block_size:
            self.rect.x -= 0.5

        if self.rect.y < target_y * block_size:
            self.rect.y += 0.5
        elif self.rect.y > target_y * block_size:
            self.rect.y -= 0.5

    def draw(self, screen):
        screen.blit(ghost_image, (self.rect.x, self.rect.y))

# Function to check for collisions with walls
def check_collision(x, y):
    return maze[int(y)][int(x)] == "#"

# Function to check for collisions at a specific position
def check_wall(x, y):
    return check_collision(x, y) or check_collision(x + 0.8, y) or check_collision(x, y + 0.8)

# Define racecar's starting position (grid coordinates)
racecar_x, racecar_y = 1, 1
racecar_speed = 0.05

# Initialize ghosts
ghosts = [Ghost(random.randint(1, len(maze[0]) - 2), random.randint(1, len(maze) - 2)) for _ in range(3)]

# Game loop
running = True
racecar_dx, racecar_dy = 0, 0
caught = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                racecar_dx, racecar_dy = 0, -racecar_speed
            elif event.key == pygame.K_DOWN:
                racecar_dx, racecar_dy = 0, racecar_speed
            elif event.key == pygame.K_LEFT:
                racecar_dx, racecar_dy = -racecar_speed, 0
            elif event.key == pygame.K_RIGHT:
                racecar_dx, racecar_dy = racecar_speed, 0

    # Update racecar's position
    new_x = racecar_x + racecar_dx
    new_y = racecar_y + racecar_dy

    # Check for collision with walls
    if not check_wall(new_x, racecar_y):
        racecar_x = new_x
    if not check_wall(racecar_x, new_y):
        racecar_y = new_y

    # Move ghosts and check for collision with the racecar
    for ghost in ghosts:
        ghost.move_towards(racecar_x, racecar_y)
        if ghost.rect.colliderect(pygame.Rect(racecar_x * block_size, racecar_y * block_size, block_size, block_size)):
            caught = True

    # Drawing
    screen.fill(BLACK)
    draw_maze(screen, maze)
    draw_racecar(screen, racecar_x, racecar_y)
    for ghost in ghosts:
        ghost.draw(screen)

    # Show message if caught
    if caught:
        font = pygame.font.SysFont(None, 48)
        text = font.render("Caught by a ghost!", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
