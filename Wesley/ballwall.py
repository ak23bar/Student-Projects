import pygame
import math
import random

# Initialize variables
z = 0
r = 0
b = 0
l = 0
STOP = False
pos = False
clock = pygame.time.Clock()
stack = []
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ballsize = 80
start = (50, 50)
current_pos = (50, 50)
end = 2
line_draw = False
speed = 35
slow_rate = 1.7

# Game display
pygame.init()

# Get screen dimensions
info = pygame.display.Info()
screen_width, screen_height = info.current_w , info.current_h 

# Set display to fullscreen with detected width and height
screen = pygame.display.set_mode((screen_width, screen_height))

screen.fill(BLACK)
pygame.display.set_caption('The Bouncing Ball')

# Walls
def draw_walls():
    floor = pygame.draw.line(screen, WHITE, (screen_width - 50, screen_height - 50), (50, screen_height - 50), 8)
    ceiling = pygame.draw.line(screen, WHITE, (50, 50), (screen_width - 50, 50), 8)
    wall_left = pygame.draw.line(screen, WHITE, (50, 50), (50, screen_height - 50), 8)
    wall_right = pygame.draw.line(screen, WHITE, (screen_width - 50, screen_height - 50), (screen_width - 50, 50), 8)

# Ball class
class Ball:
    def __init__(self, x, y, xvel, yvel):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color
        self.radius = ballsize//2  # Radius of the ball

    def update(self):
        # Bounce logic for walls
        # Right wall collision (using screen_width)
        if self.x + ballsize > screen_width - 50:  # Right wall
            self.x = screen_width - 50 - ballsize
            self.xvel = -self.xvel / slow_rate
        # Left wall collision
        elif self.x < 50:  # Left wall
            self.x = 50
            self.xvel = -self.xvel / slow_rate

        # Floor collision (using screen_height)
        if self.y + ballsize > screen_height - 50:  # Floor
            self.y = screen_height - 50 - ballsize
            self.yvel = -self.yvel / slow_rate
        # Ceiling collision
        elif self.y < 50:  # Ceiling
            self.y = 50
            self.yvel = -self.yvel / slow_rate

        # Update position
        self.x += self.xvel
        self.y += self.yvel

        # Apply friction
        self.xvel = self.xvel / 1.007
        self.yvel = self.yvel / 1.007

    def draw(self):
        pygame.draw.ellipse(screen, self.color, [self.x, self.y, ballsize, ballsize], 0)  # Use the ball's color

    def collide_with(self, other):
        # Calculate the distance between the centers of the two balls
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Check if the balls are colliding
        if distance <= self.radius + other.radius:
            # Calculate the angle of collision
            angle = math.atan2(dy, dx)

            # Calculate the components of the velocity vectors
            v1 = math.sqrt(self.xvel ** 2 + self.yvel ** 2)
            v2 = math.sqrt(other.xvel ** 2 + other.yvel ** 2)

            # Calculate the direction of the velocity vectors
            dir1 = math.atan2(self.yvel, self.xvel)
            dir2 = math.atan2(other.yvel, other.xvel)

            # Calculate the new velocities using elastic collision formulas
            new_v1x = v1 * math.cos(dir1 - angle)
            new_v1y = v1 * math.sin(dir1 - angle)
            new_v2x = v2 * math.cos(dir2 - angle)
            new_v2y = v2 * math.sin(dir2 - angle)

            # Final velocities after collision
            final_v1x = new_v2x
            final_v2x = new_v1x
            final_v1y = new_v1y
            final_v2y = new_v2y

            # Convert velocities back to Cartesian coordinates
            self.xvel = math.cos(angle) * final_v1x - math.sin(angle) * final_v1y
            self.yvel = math.sin(angle) * final_v1x + math.cos(angle) * final_v1y
            other.xvel = math.cos(angle) * final_v2x - math.sin(angle) * final_v2y
            other.yvel = math.sin(angle) * final_v2x + math.cos(angle) * final_v2y

            # Move the balls apart to avoid sticking
            overlap = (self.radius + other.radius) - distance
            self.x -= overlap * (dx / distance) / 2
            self.y -= overlap * (dy / distance) / 2
            other.x += overlap * (dx / distance) / 2
            other.y += overlap * (dy / distance) / 2

# List to store balls
balls = []

# Game run
rungame = True
while rungame:
    screen.fill(BLACK)
    draw_walls()

    # Draw the line dynamically if line_draw is True
    if line_draw is True:
        current_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, WHITE, start, current_pos, 6)  # Draw the line
        #print("Current position:", current_pos)  # Print the current mouse position

    # Update and draw all balls (always, regardless of line_draw)
    for i, ball in enumerate(balls):
        ball.update()
        ball.draw()

        # Check for collisions with other balls
        for other_ball in balls[i + 1:]:
            ball.collide_with(other_ball)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rungame = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                start = pygame.mouse.get_pos()
                STOP = False
                pos = True
                (x, y) = start
                if x >= screen_width or x <= 50 or y >= screen_height or y <= 50:
                    line_draw = False
                    STOP = True
                else:
                    line_draw = True
                    #print("Start", start)
        # Handle mouse button up (end drawing)
        if event.type == pygame.MOUSEBUTTONUP:
            if STOP == False:
                end = pygame.mouse.get_pos()
                line_draw = False
                #print("End:", end)
                (x, y) = start
                direction = (end[0] - start[0], end[1] - start[1])
                magnitude = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
                if magnitude != 0:
                    xvel = (direction[0] / magnitude) * speed
                    yvel = (direction[1] / magnitude) * speed
                    # Create a new ball with a random color and add it to the list
                    balls.append(Ball(x, y, xvel, yvel))

    clock.tick(60)
    pygame.display.update()

pygame.quit()