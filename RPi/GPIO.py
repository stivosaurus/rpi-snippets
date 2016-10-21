""" Fake RPi.GPIO module """

BOARD = 'board'
BCM = 'bcm'
OUT = 0
IN = 1
HIGH = 1
LOW = 0

def setmode( param ):
    pass

def setwarnings( param ):
    pass

def setup( channels, dir, initial=LOW):
    pass

def output( channels, state):
    pass

def input(channels, state):
    pass

def cleanup(channels=None):
    pass






