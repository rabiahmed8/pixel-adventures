import pygame
import sys
import random

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

from freetype import *


pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 35.5, 50
CAR_SPEED = 12
OBSTACLE_SPEED = 3
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50

# Colors
WHITE = 'cyan'
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Adventures")

# Load game assets
# car_image = pygame.image.load("pngegg.png")
# car_image = pygame.transform.scale(car_image, (CAR_WIDTH, CAR_HEIGHT))
obstacle_image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obstacle_image.fill(WHITE)

display = (WIDTH, HEIGHT)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)
glClearColor(0, 0, 0, 1)

# # Initialize game variables
car_x = WIDTH // 2 - CAR_WIDTH // 2
car_y = HEIGHT - CAR_HEIGHT
obstacles = []
score = 0

# Load a font using FreeType
font_size = 24
font = pygame.font.Font("Montserrat-Regular.ttf", font_size)

def draw_car():
    glBegin(GL_QUADS)
    glVertex2f(car_x, car_y)
    glVertex2f(car_x + CAR_WIDTH, car_y)
    glVertex2f(car_x + CAR_WIDTH, car_y + CAR_HEIGHT)
    glVertex2f(car_x, car_y + CAR_HEIGHT)
    glEnd()

def draw_obstacle(ox, oy):
    glBegin(GL_QUADS)
    glVertex2f(ox, oy)
    glVertex2f(ox + OBSTACLE_WIDTH, oy)
    glVertex2f(ox + OBSTACLE_WIDTH, oy + OBSTACLE_HEIGHT)
    glVertex2f(ox, oy + OBSTACLE_HEIGHT)
    glEnd()

def draw_transparent_text(text, x, y, transparency):
    glColor4f(1, 1, 1, transparency)
    glRasterPos2f(x, y)

    for char in text:
        char_surface = font.render(char, True, (255, 255, 255))
        char_data = pygame.image.tostring(char_surface, 'RGBA', True)
        width, height = char_surface.get_width(), char_surface.get_height()

        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, char_data)

font = pygame.font.Font("Montserrat-Regular.ttf", 36)  # Replace with the path to your font file

# Function to draw text on the screen
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Handle user input to move the car
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= CAR_SPEED
    if keys[pygame.K_RIGHT] and car_x < WIDTH - CAR_WIDTH:
        car_x += CAR_SPEED

    # Generate obstacles
    if random.randint(1, 100) < 5:
        obstacle_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
        obstacle_y = -OBSTACLE_HEIGHT
        obstacles.append((obstacle_x, obstacle_y))

    # Move and remove obstacles
    for i, (ox, oy) in enumerate(obstacles):
        if score<=20:
            obstacles[i] = (ox, oy + OBSTACLE_SPEED)
        elif score<=40:
            obstacles[i] = (ox, oy + OBSTACLE_SPEED+5)
        elif score<=60:
            obstacles[i] = (ox, oy + OBSTACLE_SPEED+15)
        if oy > HEIGHT:
            obstacles.pop(i)
            score += 1

    # Collision detection
    car_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
    for ox, oy in obstacles:
        obstacle_rect = pygame.Rect(ox, oy, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        if car_rect.colliderect(obstacle_rect):
            running = False

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the car
    # glClear(car_image, (car_x, car_y))
    draw_car()

    # Draw obstacles
    for ox, oy in obstacles:
        draw_obstacle(ox, oy)

    # Display score
    draw_text(f"Score: {score}", WHITE, 100, 10)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)


# Game over screen
glClear(GL_COLOR_BUFFER_BIT)
draw_text("Game Over", WHITE, WIDTH // 2, HEIGHT // 2 - 50)
draw_text(f"Score: {score}", WHITE, WIDTH // 2, HEIGHT // 2 + 50)
pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(3000)

# Quit Pygame
pygame.quit()
sys.exit()