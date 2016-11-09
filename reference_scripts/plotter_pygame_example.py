import pygame
import sys
import os
from pygame.locals import *
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARKGRAY = (64, 64, 64)
GRAY = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)
MOUSE_LEFT = 1  # adding variables for left and right
MOUSE_RIGHT = 3  # mouse clicks see code left_right_mouse.py
# in references
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


def end_program():
    sys.exit()


def do_nothing():
    pass


def show_pointer_coords(screen, x, y):
    # pointer
    pygame.draw.ellipse(screen, GREEN, [1 + x - 5, y - 5, 10, 10], 1)


def show_x_y(screen, x, y):
    coord = myfont.render("Coords = X-%i Y-%i" % (x - 300, y - 100), 3, BLUE)
    screen.blit(coord, (115, 5))
    coord = myfont.render("Coords = X-%i Y-%i" % (x - 300, y - 100), 2, WHITE)
    screen.blit(coord, (116, 6))
    credit = myfont.render("By Stiv & Berg", 3, BLUE)
    screen.blit(credit, (20, 580))
    credit = myfont.render("By Stiv & Berg", 3, WHITE)
    screen.blit(credit, (22, 582))


def mouse_pos(screen):
    mousex, mousey = pygame.mouse.get_pos()
    #mouse_pos = myfont.render("Mouse Position = %i %i"%(mousex-300, mousey-100), 3,BLUE)
    #screen.blit(mouse_pos, (200, 5))
    #mouse_pos = myfont.render("Mouse Position = %i %i"%(mousex-300, mousey-100), 3,WHITE)
    #screen.blit(mouse_pos, (201, 6))
    if mousex <= 300 or mousex >= 1000 or mousey <= 100 or mousey >= 600:

                # make mouse change if outside box but needs work
                # TODO fix mouse design or change mouse colour when it leaves
                # coord box
        pygame.mouse.set_visible(1)
    else:
        pygame.mouse.set_visible(1)
        mouse_pos = myfont.render(
            "Mouse Position = %i %i" %
            (mousex - 300, mousey - 100), 3, BLUE)
        screen.blit(mouse_pos, (350, 5))
        mouse_pos = myfont.render(
            "Mouse Position = %i %i" %
            (mousex - 300, mousey - 100), 3, WHITE)
        screen.blit(mouse_pos, (351, 6))


def draw_screen_boarder(screen):
    pygame.draw.rect(screen, LIGHTGRAY, (300, 100, 700, 500), 2)


def draw_button(screen, text, coords, action=0):
    # command list for actions maybe use sys or os

    command = [
        'exit()',
        'donothing',
        'donothing',
        'donothing',
        'donothing',
        'donothing',
        'donothing',
        'donothing',
        'donothing',
        'donothing',
        'donothing',
        'donothing',
        'donothing']
    button = pygame.draw.rect(screen, LIGHTGRAY, coords, 0)
    button = pygame.draw.rect(screen, BLUE, coords, 2)
    screen.blit(buttonfont.render(text, True, (0, 0, 0)),
                (coords[0] + 5, coords[1]))
    if button.collidepoint(pygame.mouse.get_pos()):
        button = pygame.draw.rect(screen, GRAY, coords, 0)
        button = pygame.draw.rect(screen, WHITE, coords, 2)

        screen.blit(buttonfont.render(text, True, (200, 200, 200)),
                    (coords[0] + 5, coords[1]))
        # adding left and right mouse button test if elif
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT:
            button = pygame.draw.rect(screen, DARKGRAY, coords, 0)
            button = pygame.draw.rect(screen, BLUE, coords, 2)
            screen.blit(buttonfont.render(text, True, (RED)),
                        (coords[0] + 5, coords[1]))
            print command[action]

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_RIGHT:
            print 'right'

    else:
        pass

# ADDED left mouse click


def draw_triangle(coords, direction):
    axis_direction = [('left'), ('right'), ('up'), ('down')]
    triangle = pygame.draw.polygon(screen, LIGHTGRAY, coords, 0)
    triangle = pygame.draw.polygon(screen, WHITE, coords, 2)
    if triangle.collidepoint(pygame.mouse.get_pos()):
        triangle = pygame.draw.polygon(screen, DARKGRAY, coords, 2)
        if triangle.collidepoint(pygame.mouse.get_pos(
        )) and event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT:
            triangle = pygame.draw.polygon(screen, GRAY, coords, 0)
            triangle = pygame.draw.polygon(screen, BLUE, coords, 2)
            # do_command(axis_direction[direction])
            print axis_direction[direction]

# ADDED left mouse click


def ok_button():
    okbutton = pygame.draw.ellipse(screen, GRAY, [140, 60, 80, 80], 0)
    okbutton = pygame.draw.ellipse(screen, LIGHTGRAY, [145, 65, 70, 70], 0)
    okbutton = pygame.draw.ellipse(screen, WHITE, [140, 60, 80, 80], 2)
    if okbutton.collidepoint(pygame.mouse.get_pos()):
        okbutton = pygame.draw.ellipse(screen, DARKGRAY, [140, 60, 80, 80], 5)
        if okbutton.collidepoint(pygame.mouse.get_pos(
        )) and event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT:
            okbutton = pygame.draw.ellipse(screen, BLUE, [140, 60, 80, 80], 5)
            print 'ok'

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

# set font

buttonfont = pygame.font.SysFont("Viga", 25)
myfont = pygame.font.SysFont("monospace", 16)

# -------- Main Program Loop -----------
# we can try and use the main.py program but
# it also has a loop to run inside and hence
# we have a delema!!!!
# so our while loop has to be a subprocess
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
        # mouse position when left clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            # make sure clicking outside the box has no effect
            if mouseX <= 300 or mouseX >= 1000 or mouseY <= 100 or mouseY >= 600:
                # do nothing
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

    # THIS  makes sure the pointer stay inside the limits
    if x_coord >= 1000:
        x_coord = 1000
    if x_coord <= 300:
        x_coord = 300

    if y_coord >= 600:
        y_coord = 600
    if y_coord <= 100:
        y_coord = 100
    # print(x_coord, y_coord)#show where pointer is in console

    # --- Drawing Code

    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)

    show_pointer_coords(screen, x_coord, y_coord)
    show_x_y(screen, x_coord, y_coord)
    mouse_pos(screen)
    draw_screen_boarder(screen)
    # TODO fix the action function for the buttons
    pos = 30
    Button_text = [
        'Exit',
        'Save',
        'Get File',
        'Circle',
        'Line',
        'Rectangle',
        'Arc',
        'button7',
        'button8',
        'button9',
        'button0',
        'button1']  # these are the text for the buttons
    # these are the function keys for the buttons
    Action = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # TODO add the method to talk to the stepper controller or to main
    # added a for loop in button actions
    for i in range(len(Button_text)):
        draw_button(screen, Button_text[i], (20, 150 + pos * i, 90, 20), Action[i])

    draw_triangle([[100, 100], [140, 140], [140, 60]], LEFT)
    draw_triangle([[260, 100], [220, 140], [220, 60]], RIGHT)
    #draw_triangle([[260, 100], [220, 140],[220, 60]], 2)
    draw_triangle([[140, 60], [220, 60], [180, 20]], UP)
    draw_triangle([[220, 140], [140, 140], [180, 180]], DOWN)
    ok_button()
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
