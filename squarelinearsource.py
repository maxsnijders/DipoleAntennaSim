import source
import numpy as np;
import math;
import signals as sig;
from scipy import signal as scipy_sig;

class SquareLinearSource(source.Source):
	frequency = 1;
	amplitude = 1;
	phase0 	  = 0;
	
	def signal(self, time):
		return self.amplitude * scipy_sig.square(self.frequency * 2 * math.pi * time + self.phase0);


	def polarisation(self, time):
		return 0;

	def __init__(self, x, y, z, amplitude = 1, frequency = 1, phase0 = 0):
		self.x = x;
		self.y = y;
		self.z = z;
		
		self.amplitude = amplitude;
		self.frequency = frequency;
		self.phase0 = phase0;

		
