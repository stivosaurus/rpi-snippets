import pygame
from pygame.locals import *
import button
import fborx

pygame.init()

# this will open a 800x800 window if xserver is running or fullscreen fb if not
screen = fborx.getScreen(800,800)

#### Point 1
# this will create a button
myButton = pygbutton.PygButton(Rect(100,100,100,100), 'Text')

#### Point 2
myButton.draw(screen)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get(): # event handling loop
        #### Point 3
        # handleEvent(event) returns an array with the button events that happened
        # button events are enter,exit,move,down,up and click
        if 'click' in myButton.handleEvent(event):
            running = False
pygame.quit()
