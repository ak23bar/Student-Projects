import pygame
import random
import math

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 2400, 1800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BG = (15, 15, 25)

# Colors
RED = (255, 50, 50)
BLUE = (100, 200, 255)
ORANGE = (255, 150, 50)
PURPLE = (200, 100, 255)
PINK = (255, 100, 200)
LIGHT_PINK = (255, 180, 200)
CYAN = (100, 255, 255)
YELLOW = (255, 255, 100)
GREEN = (100, 255, 150)
SILVER = (190, 190, 200) 
GOLD = (218, 165, 32)    
SKINWALKER_PURPLE = (40, 0, 60)
KNIGHT_GRAY = (60, 60, 60) 
TRIPMINE_GLOW = (180, 0, 255)
DOZER_YELLOW = (255, 230, 50) 
DOZER_GLOW = (255, 255, 200)

# Game Balance
PLAYER_SPEED = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Nullscape: Mart's Journey")
clock = pygame.time.Clock()

# --- DRAWING FUNCTIONS ---

def draw_blob(surface, x, y, size, color, glow=True):
    if glow:
        glow_surface = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
        glow_color = (*color, 30)
        pygame.draw.circle(glow_surface, glow_color, (size * 1.5, size * 1.5), size * 1.3)
        surface.blit(glow_surface, (x - size * 1.5, y - size * 1.5))
    
    pygame.draw.ellipse(surface, color, (x - size, y - size * 0.8, size * 2, size * 1.8))
    highlight_color = tuple(min(c + 60, 255) for c in color)
    pygame.draw.ellipse(surface, highlight_color, (x - size * 0.6, y - size * 0.6, size * 1.2, size * 0.8))
    
    eye_y = y - size * 0.2
    pygame.draw.circle(surface, BLACK, (int(x - size * 0.3), int(eye_y)), max(2, size // 6))
    pygame.draw.circle(surface, BLACK, (int(x + size * 0.3), int(eye_y)), max(2, size // 6))
    mouth_y = y + size * 0.2
    pygame.draw.circle(surface, BLACK, (int(x), int(mouth_y)), max(2, size // 8))

def draw_baby(surface, x, y, size, charging=False):
    glow_surface = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
    glow_color = (255, 100, 200, 60) if charging else (200, 100, 255, 40)
    pygame.draw.circle(glow_surface, glow_color, (size * 2, size * 2), size * 1.8)
    surface.blit(glow_surface, (x - size * 2, y - size * 2))
    pygame.draw.circle(surface, LIGHT_PINK, (int(x), int(y)), size)
    pygame.draw.circle(surface, (180, 100, 255), (int(x), int(y + size * 0.3)), int(size * 0.8))
    eye_y = y - size * 0.2
    pygame.draw.circle(surface, CYAN, (int(x - size * 0.35), int(eye_y)), max(3, size // 4))
    pygame.draw.circle(surface, CYAN, (int(x + size * 0.35), int(eye_y)), max(3, size // 4))
    pygame.draw.circle(surface, BLACK, (int(x - size * 0.35), int(eye_y)), max(2, size // 6))
    pygame.draw.circle(surface, BLACK, (int(x + size * 0.35), int(eye_y)), max(2, size // 6))
    mouth_y = y + size * 0.3
    pygame.draw.circle(surface, BLACK, (int(x), int(mouth_y)), max(3, size // 5))

def draw_skinwalker(surface, x, y, size):
    glow_surface = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
    pygame.draw.circle(glow_surface, (80, 0, 100, 50), (size * 2, size * 2), size * 1.5)
    surface.blit(glow_surface, (x - size * 2, y - size * 2))
    rect = pygame.Rect(x - size, y - size * 1.2, size * 2, size * 2.4)
    pygame.draw.ellipse(surface, SKINWALKER_PURPLE, rect)
    eye_y = y - size * 0.5
    pygame.draw.circle(surface, WHITE, (int(x - size * 0.4), int(eye_y)), size // 4)
    pygame.draw.circle(surface, WHITE, (int(x + size * 0.4), int(eye_y)), size // 4)
    jaw_rect = pygame.Rect(x - size * 0.5, y - size * 0.1, size, size * 0.8)
    pygame.draw.rect(surface, BLACK, jaw_rect, border_radius=5)
    for i in range(1, 4):
        line_y = y - size * 0.1 + (i * (size * 0.2))
        pygame.draw.line(surface, WHITE, (x - size * 0.4, line_y), (x + size * 0.4, line_y), 2)

def draw_bell(surface, x, y, size):
    glow_surface = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
    pygame.draw.circle(glow_surface, (*SILVER, 50), (size * 2, size * 2), size * 1.5)
    surface.blit(glow_surface, (x - size * 2, y - size * 2))
    rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
    pygame.draw.arc(surface, SILVER, rect, 0, 3.14, size) 
    pygame.draw.rect(surface, SILVER, (x - size, y, size * 2, size * 0.5)) 
    pygame.draw.rect(surface, GOLD, (x - size * 1.2, y + size * 0.5, size * 2.4, size * 0.3))
    for i in range(5):
        spike_x = (x - size) + (i * (size * 0.5))
        pygame.draw.polygon(surface, GOLD, [(spike_x, y + size * 0.8), (spike_x + 10, y + size * 1.2), (spike_x + 20, y + size * 0.8)])
    pygame.draw.circle(surface, BLACK, (int(x - size * 0.4), int(y - size * 0.2)), size // 5)
    pygame.draw.circle(surface, BLACK, (int(x + size * 0.4), int(y - size * 0.2)), size // 5)

def draw_springer(surface, x, y, size, z_height=0):
    draw_y = y - z_height
    if z_height > 0:
        shadow_size = size * (1 - (z_height / 300))
        if shadow_size > 0:
            pygame.draw.ellipse(surface, (10, 10, 10, 100), (x - shadow_size, y - shadow_size * 0.5, shadow_size * 2, shadow_size))
    base_rect = pygame.Rect(x - size * 0.6, draw_y + size * 0.5, size * 1.2, size * 0.4)
    pygame.draw.rect(surface, (40, 40, 40), base_rect, border_radius=5)
    points = [
        (x - size * 0.4, draw_y + size * 0.5), (x + size * 0.4, draw_y + size * 0.5),
        (x + size * 0.3, draw_y - size * 0.2), (x + size * 0.6, draw_y - size * 0.4),
        (x + size * 0.3, draw_y - size * 0.8), (x + size * 0.1, draw_y - size * 1.0),
        (x - size * 0.4, draw_y - size * 0.6), (x - size * 0.5, draw_y + size * 0.2),
    ]
    pygame.draw.polygon(surface, KNIGHT_GRAY, points) 
    pygame.draw.polygon(surface, RED, points, 2) 
    pygame.draw.circle(surface, RED, (int(x + size * 0.1), int(draw_y - size * 0.6)), 3)

def draw_tripmine(surface, x, y, size, pulse_offset):
    pulse = (math.sin(pulse_offset) + 1.2) * 0.5
    glow_size = int(size * (1.5 + pulse * 0.3))
    glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
    pygame.draw.circle(glow_surface, (*TRIPMINE_GLOW, 60), (glow_size, glow_size), glow_size)
    pygame.draw.circle(glow_surface, (*TRIPMINE_GLOW, 100), (glow_size, glow_size), int(glow_size * 0.6))
    surface.blit(glow_surface, (x - glow_size, y - glow_size))
    points = []
    for i in range(6):
        angle = math.radians(30 + 60 * i) 
        px = x + size * math.cos(angle)
        py = y + size * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(surface, BLACK, points)
    pygame.draw.polygon(surface, (200, 150, 255), points, 2) 
    star_points = []
    for i in range(8):
        rad = size * 0.6 if i % 2 == 0 else size * 0.3
        angle = math.radians(i * 45 + pulse_offset * 50) 
        sx = x + rad * math.cos(angle)
        sy = y + rad * math.sin(angle)
        star_points.append((sx, sy))
    pygame.draw.polygon(surface, TRIPMINE_GLOW, star_points)

def draw_dozer(surface, x, y, size, state):
    glow_color = DOZER_GLOW
    if state == "WARNING": glow_color = (255, 200, 100)
    elif state == "ATTACK": glow_color = (255, 50, 50) 
    
    glow_surf = pygame.Surface((size*2.6, size*2.6), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (*glow_color, 100), (size*1.3, size*1.3), size*1.2)
    pygame.draw.circle(glow_surf, (*glow_color, 50), (size*1.3, size*1.3), size*1.3)
    for _ in range(10):
        off_x = random.randint(-5, 5)
        off_y = random.randint(-5, 5)
        pygame.draw.circle(glow_surf, (*glow_color, 20), (size*1.3 + off_x, size*1.3 + off_y), size*1.1)
    
    surface.blit(glow_surf, (x - size*1.3, y - size*1.3))
    pygame.draw.circle(surface, DOZER_YELLOW, (x, y), size)
    pygame.draw.arc(surface, BLACK, (x - size*0.5, y - size*0.2, size*0.3, size*0.3), 0, 3.14, 2)
    pygame.draw.arc(surface, BLACK, (x + size*0.2, y - size*0.2, size*0.3, size*0.3), 0, 3.14, 2)
    pygame.draw.arc(surface, BLACK, (x - size*0.4, y + size*0.1, size*0.8, size*0.5), 3.14, 6.28, 3)

# --- CLASSES ---

class Camera:
    def __init__(self):
        self.x = 0; self.y = 0
    def update(self, target_x, target_y):
        self.x = target_x - SCREEN_WIDTH // 2; self.y = target_y - SCREEN_HEIGHT // 2
        self.x = max(0, min(self.x, MAP_WIDTH - SCREEN_WIDTH)); self.y = max(0, min(self.y, MAP_HEIGHT - SCREEN_HEIGHT))

class Player:
    def __init__(self):
        self.x = MAP_WIDTH // 2; self.y = MAP_HEIGHT // 2
        self.size = 25; self.speed = PLAYER_SPEED
        self.vx = 0; self.vy = 0
        self.push_vx = 0; self.push_vy = 0 
        self.color = BLUE; self.bob_offset = 0; self.bob_speed = 0.15
        self.history = [(self.x, self.y)]
        self.max_history = 300 

    def move(self, keys):
        input_vx = 0
        input_vy = 0
        if keys[pygame.K_LEFT] and self.x > self.size * 1.5: input_vx = -self.speed
        if keys[pygame.K_RIGHT] and self.x < MAP_WIDTH - self.size * 1.5: input_vx = self.speed
        if keys[pygame.K_UP] and self.y > self.size * 1.5: input_vy = -self.speed
        if keys[pygame.K_DOWN] and self.y < MAP_HEIGHT - self.size * 1.5: input_vy = self.speed
        
        self.push_vx *= 0.9
        self.push_vy *= 0.9
        
        self.vx = input_vx + self.push_vx
        self.vy = input_vy + self.push_vy
        
        self.x += self.vx; self.y += self.vy
        self.x = max(self.size, min(MAP_WIDTH - self.size, self.x))
        self.y = max(self.size, min(MAP_HEIGHT - self.size, self.y))
        
        self.bob_offset += self.bob_speed
        self.history.append((self.x, self.y))
        
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def apply_force(self, fx, fy):
        self.push_vx = fx
        self.push_vy = fy
    
    def draw(self, camera):
        bob_y = math.sin(self.bob_offset) * 3
        screen_x = self.x - camera.x; screen_y = self.y - camera.y
        draw_blob(screen, int(screen_x), int(screen_y + bob_y), self.size, self.color, glow=True)
    
    def check_collision(self, enemy):
        dist_sq = (self.x - enemy.x)**2 + (self.y - enemy.y)**2
        min_dist_sq = (self.size + enemy.size)**2
        return dist_sq < min_dist_sq
    
    def check_goal(self, goal):
        dist_sq = (self.x - goal.x)**2 + (self.y - goal.y)**2
        min_dist_sq = (self.size + goal.size)**2
        return dist_sq < min_dist_sq

class Dozer:
    def __init__(self, x, y):
        self.x = x; self.y = y; self.size = 35
        self.state = "ROAM" # ROAM, WARNING, ATTACK
        self.timer = 180 # Start roaming
        self.vx = 2; self.vy = 2
        
    def update(self, player):
        if self.state == "ROAM":
            self.timer -= 1
            # Bounce off walls
            self.x += self.vx; self.y += self.vy
            if self.x <= 100 or self.x >= MAP_WIDTH - 100: self.vx *= -1
            if self.y <= 100 or self.y >= MAP_HEIGHT - 100: self.vy *= -1
            
            if self.timer <= 0:
                self.state = "WARNING"
                self.timer = 120 # 2 Seconds warning
        
        elif self.state == "WARNING":
            self.timer -= 1
            if self.timer <= 0:
                self.state = "ATTACK"
                self.timer = 90 # 1.5 Second kill window
                
        elif self.state == "ATTACK":
            self.timer -= 1
            # KILL CHECK: If player is moving
            speed = math.sqrt(player.vx**2 + player.vy**2)
            if speed > 0.5: # Tolerance for tiny floating point drift
                return "KILL"
            
            if self.timer <= 0:
                self.state = "ROAM"
                self.timer = 240 # Back to roaming
                
        return None

    def draw(self, camera):
        screen_x = self.x - camera.x; screen_y = self.y - camera.y
        if -100 < screen_x < SCREEN_WIDTH + 100 and -100 < screen_y < SCREEN_HEIGHT + 100:
            draw_dozer(screen, int(screen_x), int(screen_y), self.size, self.state)

class Tripmine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20 
        self.pulse = random.uniform(0, 6.28)
        self.pulse_speed = 0.05

    def update(self):
        self.pulse += self.pulse_speed

    def check_collision(self, player):
        dist_sq = (self.x - player.x)**2 + (self.y - player.y)**2
        min_dist_sq = (self.size * 0.8 + player.size * 0.8)**2 
        return dist_sq < min_dist_sq

    def draw(self, camera):
        screen_x = self.x - camera.x; screen_y = self.y - camera.y
        if -50 < screen_x < SCREEN_WIDTH + 50 and -50 < screen_y < SCREEN_HEIGHT + 50:
            draw_tripmine(screen, int(screen_x), int(screen_y), self.size, self.pulse)

class Bell:
    def __init__(self):
        self.x = 0; self.y = 0; self.size = 35
        self.teleport_timer = 0
        self.teleport_delay = 300 
    
    def update(self, player):
        self.teleport_timer -= 1
        if self.teleport_timer <= 0:
            self.teleport(player)
            
    def teleport(self, player):
        angle = random.uniform(0, 6.28)
        dist = random.uniform(200, 500)
        self.x = player.x + math.cos(angle) * dist
        self.y = player.y + math.sin(angle) * dist
        self.x = max(100, min(MAP_WIDTH - 100, self.x))
        self.y = max(100, min(MAP_HEIGHT - 100, self.y))
        self.teleport_timer = self.teleport_delay

    def check_collision(self, player):
        dist_sq = (self.x - player.x)**2 + (self.y - player.y)**2
        min_dist_sq = (self.size + player.size)**2
        return dist_sq < min_dist_sq

    def draw(self, camera):
        screen_x = self.x - camera.x; screen_y = self.y - camera.y
        if -50 < screen_x < SCREEN_WIDTH + 50 and -50 < screen_y < SCREEN_HEIGHT + 50:
            draw_bell(screen, int(screen_x), int(screen_y), self.size)

class ICBM:
    def __init__(self, level, offset_timer=0):
        self.x = 0; self.y = 0; self.blast_radius = 160; self.state = "COOLDOWN"
        self.is_hard_mode = level >= 7; self.cooldown_timer = 180 + offset_timer
        self.warning_duration = 180; self.explosion_duration = 40
        self.timer = self.cooldown_timer; self.angle = 0 
    
    def update(self, player):
        if self.state == "COOLDOWN":
            self.timer -= 1
            if self.timer <= 0: self.state = "WARNING"; self.timer = self.warning_duration; self.x = player.x; self.y = player.y
        elif self.state == "WARNING":
            self.timer -= 1; self.angle += 2
            if self.is_hard_mode and self.timer > 75:
                predict_x = player.x + (player.vx * 15); predict_y = player.y + (player.vy * 15)
                self.x += (predict_x - self.x) * 0.1; self.y += (predict_y - self.y) * 0.1
            if self.timer <= 0: self.state = "EXPLODING"; self.timer = self.explosion_duration
        elif self.state == "EXPLODING":
            self.timer -= 1
            if self.timer <= 0: self.state = "COOLDOWN"; self.timer = random.randint(200, 400)
    
    def check_hit(self, player):
        if self.state == "EXPLODING":
            dist_sq = (player.x - self.x)**2 + (player.y - self.y)**2; return dist_sq < self.blast_radius**2
        return False
    
    def check_blast(self, entity):
        if self.state == "EXPLODING":
            dist_sq = (self.x - entity.x)**2 + (self.y - entity.y)**2
            return dist_sq < (self.blast_radius + entity.size)**2
        return False

    def draw(self, camera):
        screen_x = self.x - camera.x; screen_y = self.y - camera.y
        if -200 < screen_x < SCREEN_WIDTH + 200 and -200 < screen_y < SCREEN_HEIGHT + 200:
            if self.state == "WARNING":
                urgency = (1 - (self.timer / self.warning_duration))
                is_locked = self.timer <= 75 and self.is_hard_mode
                current_color = (255, 0, 0) if is_locked else (255, int(100 * (1-urgency)), 0)
                rect_size = self.blast_radius * 2; surface = pygame.Surface((rect_size, rect_size), pygame.SRCALPHA)
                spin_speed = 5 if is_locked else 3
                pygame.draw.arc(surface, current_color, (0, 0, rect_size, rect_size), math.radians(self.angle * (spin_speed/3)), math.radians(self.angle * (spin_speed/3) + 270), 3)
                screen.blit(surface, (screen_x - self.blast_radius, screen_y - self.blast_radius))
                fill_surface = pygame.Surface((rect_size, rect_size), pygame.SRCALPHA); fill_radius = int(self.blast_radius * urgency)
                pygame.draw.circle(fill_surface, (*current_color, 50), (self.blast_radius, self.blast_radius), fill_radius)
                screen.blit(fill_surface, (screen_x - self.blast_radius, screen_y - self.blast_radius))
                if self.timer % 30 < 15:
                    font = pygame.font.Font(None, 30)
                    text = font.render("LOCKED! RUN!", True, RED) if is_locked else font.render("MISSILE LOCK", True, RED)
                    screen.blit(text, (screen_x - 60, screen_y - 10))
            elif self.state == "EXPLODING":
                progress = 1 - (self.timer / self.explosion_duration); radius = int(self.blast_radius * (0.5 + 0.5 * progress))
                pygame.draw.circle(screen, ORANGE, (int(screen_x), int(screen_y)), radius)
                pygame.draw.circle(screen, YELLOW, (int(screen_x), int(screen_y)), int(radius * 0.7))
                pygame.draw.circle(screen, WHITE, (int(screen_x), int(screen_y)), int(radius * 0.4))

class Skinwalker:
    def __init__(self, delay_frames=120, size_mult=1.0, label=""):
        self.x = 0; self.y = 0; self.size = int(25 * size_mult)
        self.delay = delay_frames; self.label = label; self.active = False; self.bob_offset = 0
    def update(self, player):
        self.bob_offset += 0.2; target_idx = len(player.history) - self.delay
        if target_idx >= 0: self.active = True; self.x, self.y = player.history[target_idx]
        else: self.active = False
    def draw(self, camera):
        if not self.active: return
        screen_x = self.x - camera.x; screen_y = self.y - camera.y; bob_y = math.sin(self.bob_offset) * 2
        if -50 < screen_x < SCREEN_WIDTH + 50 and -50 < screen_y < SCREEN_HEIGHT + 50:
            draw_skinwalker(screen, int(screen_x), int(screen_y + bob_y), self.size)
            if self.label:
                font = pygame.font.Font(None, 20); text = font.render(self.label, True, (200, 100, 255))
                screen.blit(text, (screen_x - 20, screen_y - self.size - 20))

class Enemy:
    def __init__(self, x, y, enemy_type, level_multiplier=1.0):
        self.x = x; self.y = y; self.type = enemy_type; self.alive = True; self.bob_offset = random.uniform(0, 6.28); self.bob_speed = 0.1
        raw_speed = 0
        if enemy_type == "chaser": self.size = 18; raw_speed = 2 * level_multiplier; self.color = RED; self.intelligence = 1.0
        elif enemy_type == "dasher": self.size = 15; raw_speed = 4 * level_multiplier; self.color = ORANGE; self.intelligence = 0.7
        elif enemy_type == "lurker": self.size = 22; raw_speed = 1.5 * level_multiplier; self.color = PURPLE; self.intelligence = 1.2
        elif enemy_type == "erratic": self.size = 16; raw_speed = 3 * level_multiplier; self.color = PINK; self.intelligence = 0.5; self.random_timer = 0
        elif enemy_type == "baby":
            self.size = 20; raw_speed = 0.5; self.color = LIGHT_PINK
            self.dash_speed = min(12 * level_multiplier, PLAYER_SPEED)
            self.charge_time = 0; self.charge_duration = 60; self.dash_time = 0; self.dash_duration = 30; self.is_charging = False; self.is_dashing = False; self.dash_dx = 0; self.dash_dy = 0; self.cooldown = 0; self.cooldown_duration = 120
        self.speed = min(raw_speed, PLAYER_SPEED)
    def move(self, player):
        dx = player.x - self.x; dy = player.y - self.y; dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            if self.type == "chaser" or self.type == "dasher": self.x += (dx / dist) * self.speed * self.intelligence; self.y += (dy / dist) * self.speed * self.intelligence
            elif self.type == "lurker":
                predict_x = player.x + (dx / dist) * 30 * self.intelligence; predict_y = player.y + (dy / dist) * 30 * self.intelligence
                dx_pred = predict_x - self.x; dy_pred = predict_y - self.y; dist_pred = math.sqrt(dx_pred**2 + dy_pred**2)
                if dist_pred > 0: self.x += (dx_pred / dist_pred) * self.speed; self.y += (dy_pred / dist_pred) * self.speed
            elif self.type == "erratic":
                self.random_timer += 1; 
                if self.random_timer > 30: self.random_timer = 0
                self.x += (dx / dist + random.uniform(-1,1)) * self.speed * 0.7; self.y += (dy / dist + random.uniform(-1,1)) * self.speed * 0.7
            elif self.type == "baby":
                if self.cooldown > 0: self.cooldown -= 1; self.x += (dx / dist) * self.speed * 0.5; self.y += (dy / dist) * self.speed * 0.5
                elif not self.is_charging and not self.is_dashing:
                    if dist < 400: self.is_charging = True; self.charge_time = 0; self.dash_dx = dx / dist; self.dash_dy = dy / dist
                    else: self.x += (dx / dist) * self.speed; self.y += (dy / dist) * self.speed
                elif self.is_charging:
                    self.charge_time += 1; 
                    if self.charge_time >= self.charge_duration: self.is_charging = False; self.is_dashing = True; self.dash_time = 0
                elif self.is_dashing:
                    self.x += self.dash_dx * self.dash_speed; self.y += self.dash_dy * self.dash_speed; self.dash_time += 1
                    if self.dash_time >= self.dash_duration: self.is_dashing = False; self.cooldown = self.cooldown_duration
        self.x = max(self.size * 1.5, min(MAP_WIDTH - self.size * 1.5, self.x)); self.y = max(self.size * 1.5, min(MAP_HEIGHT - self.size * 1.5, self.y)); self.bob_offset += self.bob_speed
    def draw(self, camera):
        bob_y = math.sin(self.bob_offset) * 2; screen_x = self.x - camera.x; screen_y = self.y - camera.y
        if -50 < screen_x < SCREEN_WIDTH + 50 and -50 < screen_y < SCREEN_HEIGHT + 50:
            if self.type == "baby":
                draw_baby(screen, int(screen_x), int(screen_y + bob_y), self.size, self.is_charging)
                if self.is_charging:
                    charge_percent = self.charge_time / self.charge_duration
                    pygame.draw.rect(screen, (50, 50, 50), (screen_x - 20, screen_y - self.size - 15, 40, 5))
                    pygame.draw.rect(screen, RED, (screen_x - 20, screen_y - self.size - 15, 40 * charge_percent, 5))
            else:
                draw_blob(screen, int(screen_x), int(screen_y + bob_y), self.size, self.color, glow=True)

class Springer:
    def __init__(self, x, y, level_multiplier=1.0):
        self.x = x; self.y = y
        self.target_x = x; self.target_y = y
        self.size = 30
        self.state = "IDLE" 
        self.timer = 60
        self.z_height = 0 
        self.jump_duration = 40
        self.shockwave_radius = 180
        self.crush_radius = 40
        self.start_jump_pos = (x, y)
        self.cooldown_base = 120
        self.multiplier = level_multiplier

    def update(self, player):
        if self.state == "IDLE":
            self.timer -= 1
            dx = player.x - self.x; dy = player.y - self.y
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                self.x += (dx/dist) * 0.5
                self.y += (dy/dist) * 0.5
            
            if self.timer <= 0:
                self.state = "CHARGING"
                self.timer = 60 
                lead_x = player.x + player.vx * 20
                lead_y = player.y + player.vy * 20
                self.target_x = lead_x + random.randint(-50, 50)
                self.target_y = lead_y + random.randint(-50, 50)
                self.target_x = max(50, min(MAP_WIDTH - 50, self.target_x))
                self.target_y = max(50, min(MAP_HEIGHT - 50, self.target_y))
                self.start_jump_pos = (self.x, self.y)

        elif self.state == "CHARGING":
            self.timer -= 1
            if self.timer <= 0:
                self.state = "JUMPING"
                self.timer = 0

        elif self.state == "JUMPING":
            self.timer += 1
            progress = self.timer / self.jump_duration
            if progress >= 1.0:
                self.state = "LANDING"
                self.x = self.target_x
                self.y = self.target_y
                self.z_height = 0
                return

            self.x = self.start_jump_pos[0] + (self.target_x - self.start_jump_pos[0]) * progress
            self.y = self.start_jump_pos[1] + (self.target_y - self.start_jump_pos[1]) * progress
            self.z_height = 4 * 150 * progress * (1 - progress)

        elif self.state == "LANDING":
            self.state = "IDLE"
            self.timer = max(30, int(self.cooldown_base / self.multiplier))

    def check_effect(self, player):
        if self.state == "LANDING":
            dist_sq = (self.x - player.x)**2 + (self.y - player.y)**2
            if dist_sq < self.crush_radius**2:
                return "KILL"
            elif dist_sq < self.shockwave_radius**2:
                dx = player.x - self.x
                dy = player.y - self.y
                dist = math.sqrt(dist_sq)
                if dist == 0: dist = 1
                force = 40 * (1 - (dist / self.shockwave_radius))
                player.apply_force((dx/dist) * force, (dy/dist) * force)
                return "PUSH"
        
        if self.state == "IDLE" or self.state == "CHARGING":
             dist_sq = (self.x - player.x)**2 + (self.y - player.y)**2
             if dist_sq < (self.size + player.size)**2:
                 return "KILL"
        return None

    def draw(self, camera):
        screen_x = self.x - camera.x; screen_y = self.y - camera.y
        
        if self.state == "CHARGING" or self.state == "JUMPING":
            tx = self.target_x - camera.x
            ty = self.target_y - camera.y
            pulse = (math.sin(pygame.time.get_ticks() * 0.02) + 1) * 0.5
            alpha = int(100 + 100 * pulse)
            target_surface = pygame.Surface((self.shockwave_radius * 2, self.shockwave_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(target_surface, (255, 50, 50, 50), (self.shockwave_radius, self.shockwave_radius), self.shockwave_radius, 2)
            pygame.draw.circle(target_surface, (255, 0, 0, alpha), (self.shockwave_radius, self.shockwave_radius), self.crush_radius)
            screen.blit(target_surface, (tx - self.shockwave_radius, ty - self.shockwave_radius))
            if self.state == "JUMPING":
                pygame.draw.line(screen, (100, 50, 50), (screen_x, screen_y - self.z_height), (tx, ty), 1)

        if -100 < screen_x < SCREEN_WIDTH + 100 and -100 < screen_y < SCREEN_HEIGHT + 100:
            draw_springer(screen, int(screen_x), int(screen_y), self.size, self.z_height)

class Goal:
    def __init__(self, x, y):
        self.x = x; self.y = y; self.size = 30; self.color = YELLOW; self.pulse = 0; self.pulse_speed = 0.1
    def update(self): self.pulse += self.pulse_speed
    def draw(self, camera):
        screen_x = self.x - camera.x; screen_y = self.y - camera.y; pulse_size = self.size + math.sin(self.pulse) * 5
        glow_surface = pygame.Surface((pulse_size * 4, pulse_size * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*self.color, 40), (pulse_size * 2, pulse_size * 2), pulse_size * 1.5)
        screen.blit(glow_surface, (screen_x - pulse_size * 2, screen_y - pulse_size * 2))
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), int(pulse_size))
        pygame.draw.circle(screen, CYAN, (int(screen_x), int(screen_y)), int(pulse_size * 0.7))

def spawn_enemy(level, player_x, player_y, level_multiplier):
    while True:
        x = random.randint(100, MAP_WIDTH - 100); y = random.randint(100, MAP_HEIGHT - 100)
        dist = math.sqrt((x - player_x)**2 + (y - player_y)**2)
        if dist > 300: break
    types = ["chaser"]
    if level >= 2: types.append("dasher")
    if level >= 3: types.append("lurker")
    if level >= 5: types.append("erratic")
    if level >= 7: types.append("baby")
    return Enemy(x, y, random.choice(types), level_multiplier)

def spawn_skinwalker_group(level):
    group = []
    curse_roll = random.choice(["Normal", "Closer", "Further", "Taller", "Conga"])
    if curse_roll == "Normal": group.append(Skinwalker(delay_frames=120, label="Skinwalker"))
    elif curse_roll == "Closer": group.append(Skinwalker(delay_frames=60, label="Closer")) 
    elif curse_roll == "Further": group.append(Skinwalker(delay_frames=180, label="Further")) 
    elif curse_roll == "Taller": group.append(Skinwalker(delay_frames=120, size_mult=1.5, label="Taller"))
    elif curse_roll == "Conga":
        group.append(Skinwalker(delay_frames=90, label="Conga 1"))
        group.append(Skinwalker(delay_frames=120, label="Conga 2"))
        group.append(Skinwalker(delay_frames=150, label="Conga 3"))
    return group

def create_level_enemies(level):
    difficulty_tier = (level - 1) // 3
    base_enemies = 3 + (difficulty_tier * 2)
    return min(base_enemies, 25)

def main():
    player = Player(); camera = Camera()
    level = 1; max_level = 21; checkpoint_level = 1
    enemies = []; icbms = []; skinwalkers = []; bells = []; springers = []; tripmines = []; dozers = []
    goal = None; game_over = False; level_complete = False; running = True
    screen_shake = 0
    
    def setup_level(lvl):
        nonlocal enemies, goal, icbms, skinwalkers, bells, springers, tripmines, dozers
        enemies = []; icbms = []; skinwalkers = []; bells = []; springers = []; tripmines = []; dozers = []
        player.history = [(player.x, player.y)]
        difficulty_tier = (lvl - 1) // 3
        level_multiplier = 1.0 + (difficulty_tier * 0.15)
        
        enemy_count = create_level_enemies(lvl)
        for i in range(enemy_count): enemies.append(spawn_enemy(lvl, player.x, player.y, level_multiplier))
            
        icbm_count = 1
        if lvl >= 8: icbm_count = 3
        for i in range(icbm_count): icbms.append(ICBM(lvl, offset_timer=i*120))
            
        if lvl >= 4:
            spawn_dozer = False
            if lvl >= 5 and random.random() < 0.5:
                spawn_dozer = True
            
            if spawn_dozer:
                count = 1 if lvl < 10 else 2
                for _ in range(count):
                    dx = random.randint(200, MAP_WIDTH - 200)
                    dy = random.randint(200, MAP_HEIGHT - 200)
                    dozers.append(Dozer(dx, dy))
            else:
                groups_count = 1
                if lvl >= 10: groups_count = 2
                for _ in range(groups_count): skinwalkers.extend(spawn_skinwalker_group(lvl))
        
        if lvl >= 2:
            bells.append(Bell())
            if lvl >= 9: bells.append(Bell()) 
            
        if lvl >= 3:
            springer_count = 1 + (lvl // 5)
            for _ in range(springer_count):
                sx = random.randint(100, MAP_WIDTH - 100)
                sy = random.randint(100, MAP_HEIGHT - 100)
                springers.append(Springer(sx, sy, level_multiplier))

        if lvl > 5:
            tripmine_count = 4 + (lvl - 5) * 2 
            for _ in range(tripmine_count):
                while True:
                    tmx = random.randint(100, MAP_WIDTH - 100)
                    tmy = random.randint(100, MAP_HEIGHT - 100)
                    if math.sqrt((tmx - player.x)**2 + (tmy - player.y)**2) > 400:
                        tripmines.append(Tripmine(tmx, tmy))
                        break
        
        goal_x = random.randint(200, MAP_WIDTH - 200); goal_y = random.randint(200, MAP_HEIGHT - 200)
        while math.sqrt((goal_x - player.x)**2 + (goal_y - player.y)**2) < 800:
            goal_x = random.randint(200, MAP_WIDTH - 200); goal_y = random.randint(200, MAP_HEIGHT - 200)
        goal = Goal(goal_x, goal_y)
    
    setup_level(level)
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    level = checkpoint_level; player.x = MAP_WIDTH // 2; player.y = MAP_HEIGHT // 2
                    game_over = False; level_complete = False; setup_level(level); screen_shake = 0
                if game_over and event.key == pygame.K_q: running = False
                if level_complete and event.key == pygame.K_SPACE:
                    level += 1
                    if level % 3 == 0: checkpoint_level = level
                    if level > max_level: game_over = True; level_complete = False
                    else: level_complete = False; setup_level(level); screen_shake = 0
        
        if not game_over and not level_complete:
            dozer_active_threat = any(d.state in ["WARNING", "ATTACK"] for d in dozers)

            keys = pygame.key.get_pressed()
            player.move(keys)
            
            for dozer in dozers:
                status = dozer.update(player)
                if status == "KILL": game_over = True

            if not dozer_active_threat:
                shake_x = random.randint(-8, 8) if screen_shake > 0 else 0
                shake_y = random.randint(-8, 8) if screen_shake > 0 else 0
                if screen_shake > 0: screen_shake -= 1
                
                camera.update(player.x + shake_x, player.y + shake_y)
                goal.update()
                
                if player.check_goal(goal): level_complete = True
                
                for enemy in enemies:
                    enemy.move(player)
                    if player.check_collision(enemy): game_over = True
                
                # Check ICBM Explosions against Enemies
                for icbm in icbms:
                    icbm.update(player)
                    if icbm.check_hit(player): game_over = True
                    if icbm.state == "EXPLODING":
                        # Filter out dead enemies
                        enemies[:] = [e for e in enemies if not icbm.check_blast(e)]
                        skinwalkers[:] = [s for s in skinwalkers if not icbm.check_blast(s)]
                        springers[:] = [s for s in springers if not icbm.check_blast(s)]
                        dozers[:] = [d for d in dozers if not icbm.check_blast(d)]
                
                for sw in skinwalkers:
                    sw.update(player)
                    if sw.active:
                        dist_sq = (player.x - sw.x)**2 + (player.y - sw.y)**2
                        min_dist_sq = (player.size + sw.size)**2
                        if dist_sq < min_dist_sq: game_over = True
                
                for bell in bells:
                    bell.update(player)
                    if bell.check_collision(player):
                        player.apply_force(0, -15) 
                        screen_shake = 60 
                        bell.teleport(player)
                
                for springer in springers:
                    springer.update(player)
                    effect = springer.check_effect(player)
                    if effect == "KILL":
                        game_over = True
                    elif effect == "PUSH":
                        screen_shake = 20
                
                for tm in tripmines:
                    tm.update()
                    if tm.check_collision(player):
                        game_over = True
                        screen_shake = 30
        
        screen.fill(DARK_BG)
        
        # Grid
        grid_size = 60
        start_x = -int(camera.x % grid_size)
        start_y = -int(camera.y % grid_size)
        for i in range(start_x, SCREEN_WIDTH, grid_size): pygame.draw.line(screen, (30, 30, 40), (i, 0), (i, SCREEN_HEIGHT), 1)
        for i in range(start_y, SCREEN_HEIGHT, grid_size): pygame.draw.line(screen, (30, 30, 40), (0, i), (SCREEN_WIDTH, i), 1)
        
        font_small = pygame.font.Font(None, 24)
        boundary_text = font_small.render(f"Map: {MAP_WIDTH}x{MAP_HEIGHT}", True, (80, 80, 90))
        screen.blit(boundary_text, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 30))
        
        goal.draw(camera)
        for icbm in icbms: icbm.draw(camera)
        for tm in tripmines: tm.draw(camera)
        for enemy in enemies: enemy.draw(camera)
        for sw in skinwalkers: sw.draw(camera)
        for bell in bells: bell.draw(camera)
        for springer in springers: springer.draw(camera)
        for dozer in dozers: dozer.draw(camera)
        player.draw(camera)
        
        if not game_over and any(d.state in ["WARNING", "ATTACK"] for d in dozers):
            tint = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            tint.set_alpha(30)
            tint.fill((255, 200, 0)) # Yellow tint
            screen.blit(tint, (0, 0))
            
            warn_font = pygame.font.Font(None, 60)
            warn_text = warn_font.render("DOZER WATCHING - FREEZE!", True, (255, 50, 50))
            screen.blit(warn_text, (SCREEN_WIDTH//2 - 300, 100))

        font = pygame.font.Font(None, 36)
        level_text = font.render(f"Level: {level}/{max_level}", True, WHITE)
        enemy_text = font.render(f"Enemies: {len(enemies)}", True, WHITE)
        icbm_text = font.render(f"ICBMs: {len(icbms)}", True, RED)
        
        if len(dozers) > 0:
            walker_text = font.render(f"DOZERS: {len(dozers)}", True, DOZER_YELLOW)
        else:
            walker_text = font.render(f"Skinwalkers: {len(skinwalkers)}", True, (200, 100, 255))
            
        springer_text = font.render(f"Springers: {len(springers)}", True, (255, 100, 100))
        tripmine_text = font.render(f"Tripmines: {len(tripmines)}", True, (200, 50, 255))
        checkpoint_text = font.render(f"Checkpoint: {checkpoint_level}", True, CYAN)
        
        screen.blit(level_text, (10, 10))
        screen.blit(enemy_text, (10, 50))
        screen.blit(icbm_text, (10, 90))
        screen.blit(walker_text, (10, 130))
        screen.blit(springer_text, (10, 170))
        screen.blit(tripmine_text, (10, 210))
        screen.blit(checkpoint_text, (10, 250))
        
        goal_dx = goal.x - player.x; goal_dy = goal.y - player.y
        goal_dist = math.sqrt(goal_dx**2 + goal_dy**2)
        goal_info = font.render(f"Goal: {int(goal_dist)}m", True, YELLOW)
        screen.blit(goal_info, (10, 290))
        
        if level_complete:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); overlay.set_alpha(150); overlay.fill((0, 20, 0)); screen.blit(overlay, (0, 0))
            if level % 3 == 0 and level <= max_level:
                checkpoint_font = pygame.font.Font(None, 56); checkpoint_notif = checkpoint_font.render("CHECKPOINT SAVED!", True, CYAN)
                screen.blit(checkpoint_notif, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 120))
            if level >= max_level:
                complete_font = pygame.font.Font(None, 72); complete_text = complete_font.render("ALL LEVELS COMPLETE!", True, GREEN)
                screen.blit(complete_text, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 50))
            else:
                complete_font = pygame.font.Font(None, 64); complete_text = complete_font.render(f"LEVEL {level} COMPLETE!", True, GREEN)
                next_font = pygame.font.Font(None, 36); next_text = next_font.render("Press SPACE for Next Level", True, WHITE)
                screen.blit(complete_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 50))
                screen.blit(next_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 20))
        
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); overlay.set_alpha(150); overlay.fill((20, 0, 0)); screen.blit(overlay, (0, 0))
            game_over_font = pygame.font.Font(None, 72); game_over_text = game_over_font.render("MART ABSORBED", True, RED)
            restart_font = pygame.font.Font(None, 36); restart_text = restart_font.render("Press R to Restart | Q to Quit", True, WHITE)
            level_reached = restart_font.render(f"Reached Level: {level}", True, CYAN)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 80))
            screen.blit(level_reached, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 20))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 40))
        
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()