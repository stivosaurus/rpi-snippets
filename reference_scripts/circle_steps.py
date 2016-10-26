#I have taken a simple circle plot and changed the output to a move to a position
 
from math import sin,cos,pi
import matplotlib.pyplot as plt
import time
 
# use radians instead of degrees - OBVIOUSLY!! 
list_radians = [0]
 
# from degrees to radians, the 0 is already included so
# we don't make the universe collapse by dividing by zero.
for i in range(0,360):
    float_div = 180.0/(i+1)
    list_radians.append(pi/float_div)
     
# list of coordinates for each point
MOV = 'mov'
file_write = ''
position = 0
list_x2_axis = []
list_y2_axis = []
last_position_x = 0
last_position_y = 0
# calculate coordinates 
# and append to above list
for a in list_radians:
    position += 1
    list_x2_axis.append(cos(a))
    list_y2_axis.append(sin(a))
    #print out the next position to advance to
    print MOV, int((cos(a)-last_position_x)*3000), int((sin(a)-last_position_y)*3000), 0
    add=int((cos(a)-last_position_x)*3000), int((sin(a)-last_position_y)*3000), 0
    file_write = file_write + str(add) +"\n"
    #set the old position in a variable
    last_position_x = cos(a)
    last_position_y = sin(a)
 
# set axis limits
plt.xlim(-1.5,1.5)
plt.ylim(-1.5,1.5)
 
# plot the coordinates
plt.plot(list_x2_axis,list_y2_axis,c='r')
 
# show the plot
plt.show()
#print file_write
time.sleep(10)
quit()
