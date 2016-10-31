import pygame
import sys
from pygame.locals import *
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0) 
 
def show_pointer_coords(screen, x, y):
    # pointer
    pygame.draw.ellipse(screen, GREEN, [1 + x-5, y-5, 10, 10], 1)
    
def show_x_y(screen, x, y):
    coord = myfont.render("coords = %i %i"%(x - 100, y - 30), 2,RED)
    screen.blit(coord, (5, 5))
    credit = myfont.render("By Stiv & Berg",3, BLUE)
    screen.blit(credit, (1050, 630)) 

def mouse_pos(screen):
    mousex, mousey = pygame.mouse.get_pos()
    mouse_pos = myfont.render("mouse position = %i %i"%(mousex-100, mousey-30), 2,RED)
    screen.blit(mouse_pos, (200, 5))

def draw_screen_boarder(screen):
    pygame.draw.rect(screen,GREEN,(100,30,900,610),1)


# Setup
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [1200, 650]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Plotter 2D Co-Ords")
 
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
            if event.key == pygame.K_LEFT:
                x_speed = -3
            elif event.key == pygame.K_RIGHT:
                x_speed = 3
            elif event.key == pygame.K_UP:
                y_speed = -3
            elif event.key == pygame.K_DOWN:
                y_speed = 3
        #mouse position when left clicked        
        if event.type == pygame.MOUSEBUTTONDOWN:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			#make sure clicking outside the box has no effect
			if mouseX <= 99 or mouseX >= 991 or mouseY <= 29 or mouseY >= 631:
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
    if x_coord >= 990:
        x_coord = 990
    if x_coord <= 100:
        x_coord = 100

    if y_coord >= 630:
        y_coord = 630
    if y_coord <= 30:
        y_coord = 30
    #print(x_coord, y_coord)#show where pointer is in console

    # --- Drawing Code
 
    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
 
    show_pointer_coords(screen, x_coord, y_coord)
    show_x_y(screen, x_coord, y_coord)
    mouse_pos(screen)
    draw_screen_boarder(screen)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
