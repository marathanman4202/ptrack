# ptrack
# Roy Haggerty
# Feb., 2015

import numpy as np
#from math import *

path = ''
data_file = path + 'data_ex.txt'
output_file = path + 'pathlength.txt'

data = np.genfromtxt(data_file, skip_header=1) # Read  file.  Other delimiters as delimiter = ',' or whatever
# if we exceed Horton's memory, we can use np.memmap(data_file, mode='r'....details need to be studied) to read
# the file in chunks.  Ignoring this right now, since Horton is an elephant.
particle_lines = np.shape(data)[0]  # number of lines in data file

# initialize everything
not_dead_yet_count = 1
dead_particle_count = 0
live_particle_count = 0
dead_yet = False
data_path_lengths = []
time_last = data[0,3]
x_last = data[0,0]
y_last = data[0,1]
z_last = data[0,2]
s = 0.              # distance traveled by particle

for i in range(1,particle_lines):
    time = data[i,3]
    x = data[i,0]
    y = data[i,1]
    z = data[i,2]
    if time == 0. and not dead_yet:                                             # He's not dead yet
        data_path_lengths.append(
            [x_last,y_last,z_last,time_last,s,not_dead_yet_count])
        live_particle_count += 1
        x_last = x
        y_last = y
        z_last = z   
        time_last = time
        s = 0.
        not_dead_yet_count = 1      
        if i == particle_lines:
            dead_yet = True                                                     # He feels happy      
        elif data[i+1,3] != 0.: 
            dead_yet = False                                                    # Bring out your dead!
        elif data[i+1,3] == 0.:
            dead_yet = True                                                     # He'll be stone dead in a moment.
    elif time == 0. and dead_yet:                                               # He's very ill       
        x_last = x
        y_last = y
        z_last = z   
        time_last = time
        s = 0.
        not_dead_yet_count = 1  
        dead_particle_count += 1
        if i == particle_lines:
            dead_yet = True                                                     # He feels happy      
        elif data[i+1,3] != 0.: 
            dead_yet = False                                                    # Bring out your dead!
        elif data[i+1,3] == 0.:
            dead_yet = True                                                     # He'll be stone dead in a moment.
    elif time !=0. and not dead_yet:                                            # He's getting better      
        dx = x - x_last
        dy = y - y_last
        dz = z - z_last
        s += sqrt(dx**2 + dy**2 + dz **2)
        x_last = x
        y_last = y
        z_last = z     
        time_last = time
        not_dead_yet_count += 1
    if not_dead_yet_count > 499998: dead_yet = True                             # He's dead
    if x < 0. or y < 0.: dead_yet = True                                        # He's stone dead

data_path_lengths_array = np.array(data_path_lengths)
np.savetxt(output_file,data_path_lengths_array, 
           fmt=['%15.7e','%15.7e','%15.7e','%15.7e','%15.7e','%5i'], 
           delimiter='  ',
           newline='\n', 
           header=' X  Y  Z  time  pathlength  particle_steps')

print 'successful completion'
print 'total number of particles = ', live_particle_count + dead_particle_count
print 'total number of live particles = ', live_particle_count