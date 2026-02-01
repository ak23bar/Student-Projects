import pygame
pygame.init()
screen = pygame.display.set_mode((1920,1000))
done = False
timer=3680
my_font = pygame.font.SysFont('Comic Sans MS', 300)
theclock=pygame.time.Clock()
shouldtick=0
def gettime(num):
    milliseconds=str(int(num%1*100))
    seconds=int(num%60)
    minutes=int((num%3600)/60)
    hours=int((num%43200)/3600)
    hoursextra0="0"*(2-len(str(hours)))
    minutesextra0="0"*(2-len(str(minutes)))
    secondsextra0="0"*(2-len(str(seconds)))
    return f"{hoursextra0}{hours}:{minutesextra0}{minutes}:{secondsextra0}{seconds}.{milliseconds}"
while not done:
    for event in pygame.event.get():       
        if event.type == pygame.QUIT:
            done = True
    screen.fill((255,255,255))
    Text=my_font.render(gettime(timer),False,(0,0,0))
    screen.blit(Text,(150,200))
    pygame.display.flip()
    theclock.tick(200)
    timer+=-0.01
    shouldtick+=1
pygame.quit()