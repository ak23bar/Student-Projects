import pygame, random, sys
pygame.init()

# Setup
W, H = 500, 400
screen = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Game state
score, time_left = 0, 30   # seconds
circle = [W//2, H//2, 30]  # x,y,radius

while True:
    screen.fill((255,255,255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            x,y = e.pos
            if (x-circle[0])**2 + (y-circle[1])**2 < circle[2]**2:
                score+=1
                circle = [random.randint(30,W-30), random.randint(30,H-30), 30]

    # Draw circle
    pygame.draw.circle(screen,(255,0,0),(circle[0],circle[1]),circle[2])
    # Draw score + timer
    screen.blit(font.render(f"Score:{score}",1,(0,0,0)),(10,10))
    screen.blit(font.render(f"Time:{time_left}",1,(0,0,0)),(W-120,10))

    pygame.display.flip()
    clock.tick(60)

    # Countdown
    if pygame.time.get_ticks() % 1000 < 20: time_left -= 1
    if time_left <= 0:
        screen.fill((255,255,255))
        screen.blit(font.render(f"Final Score: {score}",1,(0,0,0)),(W//2-100,H//2))
        pygame.display.flip()
        pygame.time.wait(2000)
        break
