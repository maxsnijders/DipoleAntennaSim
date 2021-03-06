import source
import numpy as np;
import math;
import signals as sig;

class HarmonicRandomSource(source.Source):
	frequency = 1;
	amplitude = 1;
	phase0 	  = 0;
	
	def signal(self, time):
		return self.amplitude * np.sin(time * self.frequency * 2 * math.pi + self.phase0);

	def polarisation(self, time):
		pol = np.random.random(len(time)) * 2 * math.pi;
		return pol;

	def __init__(self, x, y, z, amplitude = 1, frequency = 1, phase0 = 0):
		self.x = x;
		self.y = y;
		self.z = z;
		
		self.amplitude 	= amplitude;
		self.frequency 	= frequency;
		self.phase0 	= phase0;

		
