import pygame
from final_run import *
pygame.init()
screen = pygame.display.set_mode((display_height, display_width))  # create screen


agent_color=colors.LIGHTBLUE1

def make_rect(x, y):
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, 10, 10))


def make_line(x, y, color):
    if x:
        pygame.draw.line(screen, color, (x, 80), (x, racks_width-70))
    elif y:
        pygame.draw.line(screen, color, (80, y), (racks_height-70, y))

# n - Height m - Cols
def build_racks(n, m):
    y = 100
    for ro in range(0, n):
        x = 100
        for cols in range(0, m):
            for i in range(x, x+100, 20):
                for j in range(y, y+100, 20):
                    make_rect(i, j)
            draw_rack_lines(x, y)
            x += 120
        y += 120

def draw_line(n, m):
    x = 80
    for i in range(m+1):
        make_line(x, 0, colors.ORANGE)  # up
        make_line(x+10, 0, colors.ORANGE)  # down
        x += 120
    y = 80
    for i in range(n+1):
        make_line(0, y, colors.ORANGE)  # right
        make_line(0, y+10, colors.ORANGE)  # left
        y += 120



def draw_rack_lines(x,y):
    pygame.draw.line(screen,colors.ORANGE,(x+15,y-10),(x+15,y+100))     #up
    pygame.draw.line(screen,colors.ORANGE,(x+55,y-10),(x+55,y+100))     #up
    pygame.draw.line(screen,colors.ORANGE,(x+35,y-10),(x+35,y+100))     #down
    pygame.draw.line(screen,colors.ORANGE,(x+75,y-10),(x+75,y+100))     #down

    pygame.draw.line(screen,colors.ORANGE,(x-10,y+15),(x+100,y+15))      #right
    pygame.draw.line(screen,colors.ORANGE,(x-10,y+55),(x+100,y+55))      #right
    pygame.draw.line(screen,colors.ORANGE,(x-10,y+35),(x+100,y+35))      #left
    pygame.draw.line(screen,colors.ORANGE,(x-10,y+75),(x+100,y+75))      #left



running = True
counter = pygame.image.load("human.png")
i=len(Path)
while running:
    time.sleep(0.02)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break
    screen.fill((0, 0, 0))
    screen.blit(counter, (racks_height+200, racks_height+200))
    build_racks(n, m)
    draw_line(n, m)
    if i+1>0:
        i-=1
    if i>=0:
        Agent1.playerX=Path[i][0]
        Agent1.playerY=Path[i][1]

    pygame.draw.circle(screen, agent_color,(Agent1.playerX, Agent1.playerY), 2)
    pygame.display.update()
    if i==0:
        time.sleep(2)
        Path= cAgents.getBFSPath(numofrack[str((1,0,1,1))])
        i=len(Path)
        agent_color=colors.BLUE3