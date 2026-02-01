# based on a game i made in scratch
#pygame
import pygame,math
pygame.init()
x=960
y=900
screen = pygame.display.set_mode((1920,1000))
pygame.display.set_caption('0')
my_font = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()
running=True
turrets=[]
TRACK=[(0,0),(500,960),(600,700),(1000,800),(1720,900),(30,0)]
dists=[]
for seg in TRACK:
    try:
        dists.append(math.dist(seg,TRACK[TRACK.index(seg)+1]))
    except IndexError:
        pass    
print(dists)
def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect
class Turret:
    def __init__(self): 
        self.pivot=(34, 65)
        self.image=pygame.image.load('New_turretim.png')
        turrets.append(self)
        self.rotation=0
        self.pos=(500,500)
    def update(self):
        screen.blit(rot_center(self.image,self.rotation,self.pos[0],self.pos[1])[0],rot_center(self.image,self.rotation,self.pos[0],self.pos[1])[1])
class Enemy:
    def __init__(self):
        self.type='normal'
        self.color=(0,180,0)
        self.size=40
        enemies.append(self)
        self.pos=TRACK[0]
        self.speed=16
        self.progress=0
        self.angle=math.atan((TRACK[0][0]-TRACK[1][0])/(TRACK[0][1]-TRACK[1][1]))
        self.currentseg=(TRACK[0],TRACK[1],0)
        self.currentdist=dists[0]
    def update(self):
        if self.currentseg[0][0]<self.currentseg[1][0]:
            self.angle=math.atan((self.currentseg[0][1]-self.currentseg[1][1])/(self.currentseg[0][0]-self.currentseg[1][0]))
        else:
            self.angle=math.atan((self.currentseg[0][1]-self.currentseg[1][1])/(self.currentseg[0][0]-self.currentseg[1][0]))+math.pi
        if self.currentseg[0]==TRACK[-2] and self.progress>dists[-1]-30:
            enemies.remove(self)
            
        if self.progress>self.currentdist:
            self.currentseg=(None,None,self.currentseg[2]+1)
            self.currentseg=(TRACK[self.currentseg[2]],TRACK[self.currentseg[2]+1],self.currentseg[2])
            self.currentdist=dists[self.currentseg[2]]
            self.progress=0
            self.pos
        self.pos=(self.pos[0]+(self.speed*math.cos(self.angle)),self.pos[1]+(self.speed*math.sin(self.angle)))
        self.progress+=self.speed
        pygame.draw.circle(screen,self.color,self.pos,self.size)
enemies=[]
Enemy()
Turret()
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    screen.fill((30,200,30))
    for point in TRACK:
        try:
           pygame.draw.line(screen,(0,0,0),point,TRACK[TRACK.index(point)+1],10)
        except IndexError:
            pass
    for enemy in enemies:
        enemy.update()
    for turret in turrets:
        turret.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()