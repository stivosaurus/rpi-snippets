import pygame
import sys
from pygame.locals import *
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARKGRAY  = ( 64,  64,  64)
GRAY      = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)
def end_program():
    sys.exit()
def do_nothing():
    pass
def show_pointer_coords(screen, x, y):
    # pointer
    pygame.draw.ellipse(screen, GREEN, [1 + x-5, y-5, 10, 10], 1)
    
def show_x_y(screen, x, y):
    coord = myfont.render("coords = %i %i"%(x - 300, y - 100), 2,BLUE)
    screen.blit(coord, (5, 5))
    coord = myfont.render("coords = %i %i"%(x - 300, y - 100), 2,WHITE)
    screen.blit(coord, (6, 6))    
    credit = myfont.render("By Stiv & Berg",3, BLUE)
    screen.blit(credit, (20, 580))
    credit = myfont.render("By Stiv & Berg",3, WHITE)
    screen.blit(credit, (22, 582)) 

def mouse_pos(screen):
    mousex, mousey = pygame.mouse.get_pos()
    #mouse_pos = myfont.render("Mouse Position = %i %i"%(mousex-300, mousey-100), 3,BLUE)
    #screen.blit(mouse_pos, (200, 5))
    #mouse_pos = myfont.render("Mouse Position = %i %i"%(mousex-300, mousey-100), 3,WHITE)
    #screen.blit(mouse_pos, (201, 6))
    if mousex <= 300 or mousex >= 1000 or mousey <= 100 or mousey >= 600:

		#make mouse change if outside box but needs work
		#TODO fix mouse design or change mouse colour when it leaves coord box
        pygame.mouse.set_visible(1)
    else:
        pygame.mouse.set_visible(1)
        mouse_pos = myfont.render("Mouse Position = %i %i"%(mousex-300, mousey-100), 3,BLUE)
        screen.blit(mouse_pos, (290, 5))
        mouse_pos = myfont.render("Mouse Position = %i %i"%(mousex-300, mousey-100), 3,WHITE)
        screen.blit(mouse_pos, (291, 6))

def draw_screen_boarder(screen):
    pygame.draw.rect(screen,LIGHTGRAY,(300,100,700,500),2)
    
def draw_button1(screen, text, coords, action = do_nothing()):
    button1=pygame.draw.rect(screen,LIGHTGRAY,coords,0)
    button1=pygame.draw.rect(screen,BLUE,coords,2)
    screen.blit(buttonfont.render(text, True, (0,0,0)), (coords[0]+5, coords[1]))
    if button1.collidepoint(pygame.mouse.get_pos()):
        button1=pygame.draw.rect(screen,GRAY,coords,0)
        button1=pygame.draw.rect(screen,WHITE,coords,2)
        
        screen.blit(buttonfont.render(text, True, (200,200,200)), (coords[0]+5, coords[1]))
        if event.type == pygame.MOUSEBUTTONDOWN:
            button1=pygame.draw.rect(screen,DARKGRAY,coords,0)
            button1=pygame.draw.rect(screen,BLUE,coords,2)
            screen.blit(buttonfont.render(text, True, (RED)), (coords[0]+5, coords[1]))
            action
        else:
            pass
            
    else:
        pass


def draw_triangle(coords, direction):
    triangle = pygame.draw.polygon(screen, WHITE, coords, 2)
    if triangle.collidepoint(pygame.mouse.get_pos()):
        triangle = pygame.draw.polygon(screen, RED, coords, 2)
        if triangle.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
            triangle = pygame.draw.polygon(screen, BLUE, coords, 2)
            x_speed = direction

    #triangle3 = pygame.draw.polygon(screen, WHITE, [[220, 140], [140, 140],[220,60]], 2)
# Setup
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [1000, 600]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Plotter 2D coords")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(1)
 
# Speed in pixels per frame
x_speed = 0
y_speed = 0
 
# Current position
x_coord = 10
y_coord = 10

#set font

buttonfont = pygame.font.SysFont("Viga", 25)
myfont = pygame.font.SysFont("monospace", 16)
 
# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    
    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            done = True
            # User pressed down on a key
 
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            print (pygame.key.name(event.key))
            if event.key == pygame.K_LEFT:
                x_speed = -3
            elif event.key == pygame.K_RIGHT:
                x_speed = 3
            elif event.key == pygame.K_UP:
                y_speed = -3
            elif event.key == pygame.K_DOWN:
                y_speed = 3
            elif event.key == pygame.K_ESCAPE:
                sys.exit()
        #mouse position when left clicked        
        if event.type == pygame.MOUSEBUTTONDOWN:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			#make sure clicking outside the box has no effect
			if mouseX <= 300 or mouseX >= 1000 or mouseY <= 100 or mouseY >= 600:
				#do nothing
				pass
			else:
				x_coord = mouseX
				y_coord = mouseY
				print mouseX, mouseY        
 
        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0
 
    # --- Game Logic
 
    # Move the object according to the speed vector.
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed
    
    #THIS  makes sure the pointer stay inside the limits
    if x_coord >= 1000:
        x_coord = 1000
    if x_coord <= 300:
        x_coord = 300

    if y_coord >= 600:
        y_coord = 600
    if y_coord <= 100:
        y_coord = 100
    #print(x_coord, y_coord)#show where pointer is in console

    # --- Drawing Code
 
    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
 
    show_pointer_coords(screen, x_coord, y_coord)
    show_x_y(screen, x_coord, y_coord)
    mouse_pos(screen)
    draw_screen_boarder(screen)
    #TODO fix the action function for the buttons
    
    draw_button1(screen, 'exit', (20,30,60,20), do_nothing())
    draw_button1(screen, 'test1', (20,60,60,20), do_nothing())
    draw_button1(screen, 'exit1', (20,90,60,20), do_nothing())
    draw_button1(screen, 'exit2', (20,120,60,20), do_nothing())
    draw_button1(screen, 'test3', (20,150,60,20), do_nothing())
    draw_button1(screen, 'exit4', (20,180,60,20), do_nothing())
    draw_button1(screen, 'exit5', (20,210,60,20), do_nothing())
    draw_button1(screen, 'test6', (20,240,60,20), do_nothing())
    draw_button1(screen, 'exit7', (20,270,60,20), do_nothing())
    draw_button1(screen, 'exit8', (20,300,60,20), do_nothing())
    draw_button1(screen, 'test9', (20,330,60,20), do_nothing())
    draw_button1(screen, 'exit0', (20,360,60,20), do_nothing())
    draw_button1(screen, 'exit11', (20,390,60,20), do_nothing())
    draw_triangle([[100, 100], [140, 140],[140, 60]], -1)
    draw_triangle([[260, 100], [220, 140],[220, 60]], 1)
    #draw_triangle([[260, 100], [220, 140],[220, 60]], -1)
    draw_triangle([[140, 60], [220,60],[180,20]], 1)
    draw_triangle([[220, 140], [140, 140],[180, 180]], -1)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
