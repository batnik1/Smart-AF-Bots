import pygame
#import trialastar
import pygame_widgets as pw
from pygame_widgets.button import Button
pygame.init()
from Grid import Grid
screen = pygame.display.set_mode((1600, 1600))  # create screen
running = True
### Title and Icon
pygame.display.set_caption("Beti Pushpa")
target = pygame.image.load("dart.png")
Display_height=1600
Display_width=1600
matrix = Grid(Display_width, Display_height)
matrix.build_roads() 

font = pygame.font.Font('freesansbold.ttf', 13)


selected=0
color=[255,0,0]
start_button=[100,100,50]
buffer=[]
cbuffer=[]
text = font.render('END', True, (255,255,255), start_button)
while running:
    events=pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type==pygame.MOUSEBUTTONDOWN:
           x=pygame.mouse.get_pos()
           if x[0]<32 and x[0]>0 and x[1]<96 and x[1]>64:
               running = False
               start_button=[100,255,255]
               print("mamu")
               break    
           if x[0]<32 and x[0]>0 and x[1]<32 and x[1]>0:
                if selected<=3:
                    selected=selected+1
                if selected==0:
                    #draw_line(buffer)
                    color=[255,0,0]  
                elif selected==1:
                    color=[0,255,0]
                elif selected==2:
                    color=[255,255,0]
                elif selected==3:
                    color=[0,0,255]
                    
           else:
                if selected==1:
                    buffer.append(x)        # First Point
                    cbuffer.append(x)
                    selected=2
                    color=[255,255,0]
                elif selected==2:
                    buffer.append(x)        # Second Point
                    cbuffer.append(x) 
                    # pygame.draw.line(screen,(255,0,0),buffer[-1],buffer[-2])
                    selected=3
                    color=[0,0,255]
                elif selected==3:
                    buffer.append(x)        # Third Point
                    cbuffer.append(x)
                    # pygame.draw.line(screen,(255,0,0),buffer[-1],buffer[-2])
                    # pygame.draw.line(screen,(255,0,0),buffer[-2],buffer[-3])
                    selected=4
                elif selected==4:
                    buffer.append(x)        # Forth Point
                    cbuffer.append(x)
                    selected=0
                    cbuffer.clear()
                    color=[255,0,0]
    
           #blocked.append(pygame.mouse.get_pos())
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen,color, pygame.Rect(0, 0, 32, 32))
    screen.blit(target,[200,200])
    screen.blit(target,[400,400])
    screen.blit(target,[600,600])
    screen.blit(target,[800,800])
    j=0
    while j+1<len(cbuffer):
      pygame.draw.line(screen,(255,0,0),cbuffer[j],cbuffer[j+1])
      j+=1
    

    # elif selected==3:
    #     pygame.draw.line(screen,(255,0,0),buffer[-1],buffer[-2])
    # elif selected==4:
    #     pygame.draw.line(screen,(255,0,0),buffer[-1],buffer[-2])
    #     pygame.draw.line(screen,(255,0,0),buffer[-2],buffer[-3])
   
    i=0
    while i+3<len(buffer):
        #print(buffer[i],buffer[i+1],buffer[i+2],buffer[i+3])
        points = [buffer[i], buffer[i+1],buffer[i+2],buffer[i+3]]
        pygame.draw.polygon(screen, (255,0,0), points)
        i+=4
    
    pygame.draw.polygon(screen,start_button,[[0,64],[32,64],[32,96],[0,96]])
    screen.blit(text,(0,80))
    pygame.display.update()

Grid.build_obstacles(matrix,buffer)