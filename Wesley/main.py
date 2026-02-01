import pygame
from random import randint
pygame.init()
screen = pygame.display.set_mode((2000,1000))
pygame.display.set_caption('0')
clock = pygame.time.Clock()
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ball_list = []
ballprice=100
upgradecost=1
money=0
ballmoneymultiplier=1
level=1
pygame.font.init() 
my_font = pygame.font.SysFont('Comic Sans MS', 30)
pygame.key.set_repeat(3,10)
class Ball:
    def __init__(self,radius,color,xcor,ycor,xvel,yvel):
        self.radius = radius
        self.color = color
        self.xcor = xcor
        self.ycor = ycor
        self.xvel = xvel
        self.yvel = yvel
    def move(self):
        if self.xcor < 0 or self.xcor > 2000 - self.radius:
            self.xvel = -self.xvel
        if self.ycor < 0 or self.ycor > 1000 - self.radius:
            self.yvel = -self.yvel
        self.xcor += self.xvel
        self.ycor += self.yvel
        pygame.draw.ellipse(screen, self.color,
                            [self.xcor,self.ycor,2*self.radius,2*self.radius])     
for i in range (3):
    ball = Ball(randint(4,10),(randint(0,255),randint(0,255),randint(0,255)),randint(1,599),randint(1,599),randint(3,10),randint(1,7))
    ball_list.append(ball)
done = False
while not done:
    for event in pygame.event.get():       
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEWHEEL and money > ballprice:                  
            for i in range(level):
                (mouse_x,mouse_y) = pygame.mouse.get_pos()       
                ball = Ball(randint(4,10),(randint(0,255),randint(0,255),randint(0,255)),mouse_x,mouse_y,randint(3,10),randint(1,7))
                ball_list.append(ball)            
            ballprice=int(ballprice*1.01)
            money += -ballprice
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and money > upgradecost:
                ballmoneymultiplier += level
                upgradecost += 1000*level
                money += -upgradecost
            if event.key == pygame.K_q and ballmoneymultiplier>100:
                level += 1
                money=0
                ball_list=[]
                for i in range (3):
                    ball = Ball(randint(4,10),(randint(0,255),randint(0,255),randint(0,255)),randint(1,599),randint(1,599),randint(3,10),randint(1,7))
                    ball_list.append(ball)
                ballmoneymultiplier=level
                ballprice=1.5**level*100
                upgradecost=1
    pygame.display.set_caption(str(money)+"   new ball:"+str(ballprice)+"   upgrade:"+str(upgradecost)+"   multiplier:"+str(ballmoneymultiplier)+"   level:"+str(level))
    valuemeaning=["money:                  ","New ball price:      ","Upgrade:               ","Upgrade multiplier","level:                    "]
    allvalues=[money,ballprice,upgradecost,ballmoneymultiplier,level]
    screen.fill(BLUE)        
    for ball in ball_list:
        ball.move()
    valuenumber=0
    for value in allvalues:
        text_surface = my_font.render(valuemeaning[valuenumber]+str(value), False, (0, 0, 0))
        screen.blit(text_surface,(0,valuenumber*30))
        valuenumber+=1
    pygame.display.update()
    money+=len(ball_list)*ballmoneymultiplier*level
    clock.tick(60) 
pygame.quit()
