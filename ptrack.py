
# ptrack
# Roy Haggerty
# 2015

import numpy as np

path = ''
data_file = path + 'data_ex.txt'

data = np.genfromtxt(data_file, delimiter=',',skip_header=1) # Read  file

assert False