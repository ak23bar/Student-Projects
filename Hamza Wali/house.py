# starter code for pygame
import pygame

# initialize
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("my house")
clock = pygame.time.Clock()


# define colors 
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
HOUSE_COLOR = (210, 180, 140)
ROOF_COLOR = (139, 69, 19)
DOOR_COLOR = (139, 0, 0)
WINDOW_COLOR = (173, 216, 230)
SUN_COLOR = (255, 255, 0)


done = False
while not done :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    screen.fill(SKY_BLUE)   # Background sky

    # Draw grass
    pygame.draw.rect(screen, GRASS_GREEN, [0, 300, 400, 100])
    
    # Draw base
    pygame.draw.rect(screen, HOUSE_COLOR, [120, 180, 160, 120])
    
    # Roof (triangle)
    pygame.draw.polygon(screen, ROOF_COLOR, [(110, 180),(200, 100),(290, 180)])
    
    # Door
    pygame.draw.rect(screen, DOOR_COLOR, [185, 230, 30, 70])
    
    # Windows 
    pygame.draw.rect(screen, WINDOW_COLOR, [135, 200, 25, 25])
    pygame.draw.rect(screen, WINDOW_COLOR, [240, 200, 25, 25])
    
    # Sun
    pygame.draw.circle(screen, SUN_COLOR, (50, 50), 30)
    

    pygame.display.flip()
    clock.tick(60)
    
    
pygame.quit()