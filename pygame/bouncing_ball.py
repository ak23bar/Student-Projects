import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Bouncing Ball Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Ball colors list for random selection
BALL_COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, ORANGE, PINK]

# Set up the clock
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Ball class to handle multiple balls
class Ball:
    def __init__(self, x, y, radius=15, color=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color if color else random.choice(BALL_COLORS)
        self.x_vel = random.randint(-8, 8)
        self.y_vel = random.randint(-8, 8)
        # Make sure ball isn't too slow
        if abs(self.x_vel) < 3:
            self.x_vel = 3 if self.x_vel >= 0 else -3
        if abs(self.y_vel) < 3:
            self.y_vel = 3 if self.y_vel >= 0 else -3
        self.bounce_count = 0
        self.trail = []  # For trail effect
        
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
        # Add current position to trail
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > 10:  # Keep trail length manageable
            self.trail.pop(0)
    
    def bounce(self):
        # Bounce off walls
        bounced = False
        
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.x_vel = -self.x_vel
            self.bounce_count += 1
            bounced = True
            # Keep ball in bounds
            if self.x <= self.radius:
                self.x = self.radius
            else:
                self.x = SCREEN_WIDTH - self.radius
                
        if self.y <= self.radius or self.y >= SCREEN_HEIGHT - self.radius:
            self.y_vel = -self.y_vel
            self.bounce_count += 1
            bounced = True
            # Keep ball in bounds
            if self.y <= self.radius:
                self.y = self.radius
            else:
                self.y = SCREEN_HEIGHT - self.radius
        
        # Speed up slightly after bouncing (max speed limit)
        if bounced and abs(self.x_vel) < 12 and abs(self.y_vel) < 12:
            self.x_vel *= 1.02
            self.y_vel *= 1.02
            
        return bounced
    
    def draw(self, screen, show_trail=True):
        # Draw trail
        if show_trail and len(self.trail) > 1:
            for i, pos in enumerate(self.trail):
                alpha = i / len(self.trail)
                trail_radius = max(1, int(self.radius * alpha * 0.5))
                # Create a fading effect
                trail_color = tuple(int(c * alpha * 0.7) for c in self.color)
                pygame.draw.circle(screen, trail_color, pos, trail_radius)
        
        # Draw main ball
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw a highlight for 3D effect
        highlight_x = int(self.x - self.radius * 0.3)
        highlight_y = int(self.y - self.radius * 0.3)
        highlight_radius = max(1, self.radius // 3)
        pygame.draw.circle(screen, WHITE, (highlight_x, highlight_y), highlight_radius)
    
    def get_speed(self):
        return math.sqrt(self.x_vel**2 + self.y_vel**2)

# Game variables
balls = []
total_bounces = 0
game_time = 0
paused = False
show_trails = True
show_info = True
gravity_mode = False
gravity_strength = 0.2

# Create initial ball
balls.append(Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Game loop
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
    
    if not paused:
        game_time += dt
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Add a new ball at random position
                new_x = random.randint(50, SCREEN_WIDTH - 50)
                new_y = random.randint(50, SCREEN_HEIGHT - 50)
                balls.append(Ball(new_x, new_y))
            elif event.key == pygame.K_c:
                # Clear all balls except one
                if len(balls) > 1:
                    balls = [balls[0]]
                    total_bounces = balls[0].bounce_count
            elif event.key == pygame.K_r:
                # Reset everything
                balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
                total_bounces = 0
                game_time = 0
            elif event.key == pygame.K_p:
                # Pause/unpause
                paused = not paused
            elif event.key == pygame.K_t:
                # Toggle trails
                show_trails = not show_trails
            elif event.key == pygame.K_i:
                # Toggle info display
                show_info = not show_info
            elif event.key == pygame.K_g:
                # Toggle gravity mode
                gravity_mode = not gravity_mode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Add ball at mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            balls.append(Ball(mouse_x, mouse_y))
    
    if not paused:
        # Update balls
        for ball in balls:
            # Apply gravity if enabled
            if gravity_mode:
                ball.y_vel += gravity_strength
            
            ball.move()
            if ball.bounce():
                total_bounces += 1
        
        # Check for ball collisions
        for i, ball1 in enumerate(balls):
            for j, ball2 in enumerate(balls[i+1:], i+1):
                # Calculate distance between balls
                dx = ball1.x - ball2.x
                dy = ball1.y - ball2.y
                distance = math.sqrt(dx**2 + dy**2)
                
                # Check if balls are colliding
                if distance < ball1.radius + ball2.radius:
                    # Simple collision response - swap velocities
                    ball1.x_vel, ball2.x_vel = ball2.x_vel, ball1.x_vel
                    ball1.y_vel, ball2.y_vel = ball2.y_vel, ball1.y_vel
                    
                    # Separate balls to prevent sticking
                    overlap = ball1.radius + ball2.radius - distance
                    if distance > 0:
                        dx /= distance
                        dy /= distance
                        ball1.x += dx * overlap * 0.5
                        ball1.y += dy * overlap * 0.5
                        ball2.x -= dx * overlap * 0.5
                        ball2.y -= dy * overlap * 0.5
    
    # Fill the screen with black
    screen.fill(BLACK)
    
    # Draw all balls
    for ball in balls:
        ball.draw(screen, show_trails)
    
    # Draw border
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 2)
    
    # Display information
    if show_info:
        # Game stats
        stats_text = [
            f"Balls: {len(balls)}",
            f"Total Bounces: {total_bounces}",
            f"Time: {game_time:.1f}s",
            f"Gravity: {'ON' if gravity_mode else 'OFF'}"
        ]
        
        for i, text in enumerate(stats_text):
            text_surface = small_font.render(text, True, WHITE)
            screen.blit(text_surface, (10, 10 + i * 25))
        
        # Controls
        controls_text = [
            "CONTROLS:",
            "SPACE - Add ball",
            "CLICK - Add ball at mouse",
            "C - Clear extra balls",
            "R - Reset game",
            "P - Pause/Unpause",
            "T - Toggle trails",
            "I - Toggle info",
            "G - Toggle gravity"
        ]
        
        for i, text in enumerate(controls_text):
            color = YELLOW if i == 0 else WHITE
            text_surface = small_font.render(text, True, color)
            screen.blit(text_surface, (SCREEN_WIDTH - 200, 10 + i * 22))
        
        # Ball speed info
        if balls:
            speed_text = f"Ball 1 Speed: {balls[0].get_speed():.1f}"
            speed_surface = small_font.render(speed_text, True, WHITE)
            screen.blit(speed_surface, (10, SCREEN_HEIGHT - 30))
    
    # Show pause message
    if paused:
        pause_text = font.render("PAUSED - Press P to continue", True, YELLOW)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        # Draw background rectangle
        pygame.draw.rect(screen, BLACK, text_rect.inflate(20, 10))
        pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 10), 2)
        screen.blit(pause_text, text_rect)
    
    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()