#This file implements geometry utility functions
import numpy as np;

def distance_cartesian(x1, y1, z1, x2, y2, z2):
	return np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2);

