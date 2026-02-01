import pygame 
#Ammar Project goal 
#3/2/25

# Initialize Pygame 
pygame.init()

# Window settings 
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncy Ball Game")

# Colors 
WHITE = (255, 255, 255) 
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Paddle color

# Ball properties 
ball_radius = 20
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 5, 5

# Paddle properties
paddle_width, paddle_height = 100, 20
paddle_x = (WIDTH - paddle_width) // 2  # Centered paddle
paddle_y = HEIGHT - 30  # Positioned near the bottom
paddle_speed = 10

# Clock to control frame rate 
clock = pygame.time.Clock()

# Main game loop 
running = True
while running: 
    screen.fill(WHITE)  # Clear screen 
    
    # Draw ball 
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    
    # Draw paddle 
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))
    
    # Update ball position 
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # Bounce off walls
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH: 
        ball_speed_x = -ball_speed_x 
    if ball_y - ball_radius <= 0: 
        ball_speed_y = -ball_speed_y 
    if ball_y + ball_radius >= HEIGHT:
        if paddle_x <= ball_x <= paddle_x + paddle_width:  # Ball hits the paddle
            ball_speed_y = -ball_speed_y  # Bounce off the paddle
        else:
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2  # Reset ball if it hits the bottom
    
    # Event handling 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 

    # User control (paddle movement)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed
    
    # Update display 
    pygame.display.flip()
    
    # Limit frame rate to 60 FPS 
    clock.tick(60)

# Quit Pygame 
pygame.quit()
