import pygame
import random as r
pygame.init()
x=960
y=900
screen = pygame.display.set_mode((1920,1000))
pygame.display.set_caption('0')
my_font = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()
running=True
yvel=0
touchingground=True
rects=[]
enemies=[]
justdestoyedenemy=False
def inrect(x1,y1,x2,y2):
    global x
    global y
    return x1<x and y1<y and x2>x and y2>y
class Enemy:
    def __init__(self):
        self.x=960
        self.y=500
        enemies.append(self)
    def drawenemy(self):
        pygame.draw.rect(screen,(255,0,0),pygame.Rect(self.x,self.y,100,100))
    def moveenemy(self):
        self.x+=r.choice([-10,9])#move enemy
    def checkplayerpos(self):
        global yvel
        global x
        global y
        global justdestoyedenemy
        global enemybounciness
        if inrect(self.x,self.y,self.x+100,self.y+20) and not(justdestoyedenemy):
            yvel=enemybounciness
            justdestoyedenemy=True
            del enemies[enemies.index(self)]
        elif inrect(self.x,self.y+25,self.x+100,self.y+100):
            x,y=20,20
def setsettings():
    global bounciness
    global airres
    global jumpheight
    global enemybounciness
    enemybounciness=-1 # NOTE- negative number=bouncier
    jumpheight=40
    airres=1.02
    bounciness=-0.4
def rect(x1,y1,x2,y2):
    if not([x1,y1,x2,y2] in rects):
        rects.append([x1,y1,x2,y2])
    pygame.draw.rect(screen,(0,0,0),pygame.Rect(x1,y1,x2-x1,y2-y1))
def checkevents():
    global running
    global yvel
    global x
    global touchingground
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w and touchingground:
                yvel=-jumpheight
            touchingground=False
    keys=pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x+=-5
    if keys[pygame.K_d]:
        x+=5
def rungame():
    global y
    global yvel
    global x
    global touchingground
    global rects
    global justdestoyedenemy
    justdestoyedenemy=False
    Text=my_font.render(f"Num enemies:{len(enemies)}",False,(0,0,0))
    rects=[]
    y+=yvel
    yvel=yvel/airres
    yvel+=1
    if y>899:
        yvel=yvel*-0.4
        y=898
        touchingground=True
    screen.fill((230,200,200))
    pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,900,1920,100))
    drawrects()
    drawenemies()
    screen.blit(Text,(10,10))
    pygame.draw.circle(screen,(0,0,0),(x,y),5,0)
    pygame.display.flip()
    clock.tick(60)
def drawrects():
    global x
    global y
    global touchingground
    global yvel
    rect(50,800,100,880)
    rect(123,123,234,234)
    for rectangle in rects:
        if inrect(rectangle[0],rectangle[1],rectangle[2],rectangle[3]):
            yvel=yvel*bounciness
            touchingground=True

def drawenemies():
    for enemy in enemies:
        enemy.drawenemy()#draw enemies
        enemy.moveenemy()
        enemy.checkplayerpos()
setsettings()
for i in range(3):  #NOTE more enemies make it more fun   :)
    enemy1=Enemy()
while running:
    checkevents()
    rungame()
pygame.quit()