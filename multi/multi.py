#!/usr/bin/python3

from multiprocessing import Process, Queue
import os
import time


class MotorController:
    """R-Pi stepper controller."""
    def __init__(self, name, msgque):
        self.name  = name
        self.que = msgque
        self.proc = Process(target=self.run, args=())
        self.proc.start()


    def run(self):
        msg = self.que.get()
        print('msg:', msg)
        msg = self.que.get()
        print('msg:', msg)
        
    
    def step(self, steps):
        """cycle motor steps number of steps"""
        print("step %d\n")
        pass
        
    def read(self):
        x = self.que.get()
        print(x)
    

def info(title):
    print(title)
    #print('module name:', __name__)
    #print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print
    


    
def f(name):
    #info('function f')
    print('hello',   name)
    
    

if __name__ == '__main__':
    print('\t= my pid:%d '% os.getpid())
    print('\t======')
    names = ['stepX', 'stepY', 'stepZ']
    controls = []
    for nam in names:
            que = Queue()
            mc = MotorController( nam, que)
            controls.append(mc)


    # run
    for con in controls:
        con.que.put( con.name)
    time.sleep(2)
    for con in controls:
        con.que.put( con.name + '2')

    
    # time to quit
    for c in controls:
        c.proc.join()







