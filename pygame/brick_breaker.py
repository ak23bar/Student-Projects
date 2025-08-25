import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)

# Game settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
BALL_SIZE = 10
BALL_SPEED = 5
BRICK_WIDTH = 75
BRICK_HEIGHT = 25
BRICK_ROWS = 8
BRICK_COLS = 10
BRICK_PADDING = 5

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = BALL_SPEED * random.choice([-1, 1])
        self.dy = -BALL_SPEED
        self.size = BALL_SIZE
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
        # Bounce off walls
        if self.x <= self.size or self.x >= SCREEN_WIDTH - self.size:
            self.dx = -self.dx
        if self.y <= self.size:
            self.dy = -self.dy
            
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, 
                          self.size * 2, self.size * 2)

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        
    def update(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Brick:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = color
        self.destroyed = False
        
    def draw(self, screen):
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.reset_game()
        
    def reset_game(self):
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.bricks = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_won = False
        self.paused = False
        
        # Create bricks
        colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, GRAY]
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
                y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_PADDING + 50
                color = colors[row % len(colors)]
                self.bricks.append(Brick(x, y, color))
                
    def handle_collisions(self):
        ball_rect = self.ball.get_rect()
        
        # Ball-paddle collision
        if ball_rect.colliderect(self.paddle.get_rect()):
            if self.ball.dy > 0:  # Ball is moving down
                self.ball.dy = -self.ball.dy
                # Add some angle based on where ball hits paddle
                hit_pos = (self.ball.x - self.paddle.x) / self.paddle.width
                angle_factor = (hit_pos - 0.5) * 2  # -1 to 1
                self.ball.dx = BALL_SPEED * angle_factor * 1.5
                
        # Ball-brick collisions
        for brick in self.bricks:
            if not brick.destroyed and ball_rect.colliderect(brick.get_rect()):
                brick.destroyed = True
                self.score += 10
                
                # Determine collision side and bounce accordingly
                brick_rect = brick.get_rect()
                ball_center_x = self.ball.x
                ball_center_y = self.ball.y
                
                # Check which side of brick was hit
                if (ball_center_x < brick_rect.left or ball_center_x > brick_rect.right):
                    self.ball.dx = -self.ball.dx
                else:
                    self.ball.dy = -self.ball.dy
                    
                break  # Only hit one brick per frame
                
    def update(self):
        if not self.game_over and not self.game_won and not self.paused:
            keys = pygame.key.get_pressed()
            self.paddle.update(keys)
            self.ball.update()
            self.handle_collisions()
            
            # Check if ball fell off screen
            if self.ball.y > SCREEN_HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    # Reset ball position
                    self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
                    
            # Check win condition
            if all(brick.destroyed for brick in self.bricks):
                self.game_won = True
                
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw game objects
        self.ball.draw(self.screen)
        self.paddle.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
            
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        
        # Draw game state messages
        if self.paused:
            pause_text = self.big_font.render("PAUSED", True, WHITE)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
            instruction_text = self.font.render("Press P to resume", True, WHITE)
            inst_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(instruction_text, inst_rect)
            
        elif self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(restart_text, restart_rect)
            
        elif self.game_won:
            win_text = self.big_font.render("YOU WIN!", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(win_text, text_rect)
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(final_score_text, score_rect)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 90))
            self.screen.blit(restart_text, restart_rect)
            
        # Draw instructions at bottom
        if not self.game_over and not self.game_won:
            instructions = "Left/Right arrows to move, P to pause, ESC to quit"
            inst_text = pygame.font.Font(None, 24).render(instructions, True, WHITE)
            inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 20))
            self.screen.blit(inst_text, inst_rect)
            
        pygame.display.flip()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    if self.game_over or self.game_won:
                        self.reset_game()
        return True
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()