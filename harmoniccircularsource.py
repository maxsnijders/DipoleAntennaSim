import source
import numpy as np;
import math;
import signals as sig;

class HarmonicCircularSource(source.Source):
	frequency = 1;
	amplitude = 1;
	phase0 	  = 0;
	
	def signal(self, time):
		signals = np.zeros(len(time));
		signals.fill(self.amplitude);
		return signals;

	def polarisation(self, time):
		return np.cos(self.frequency * 2 * math.pi * time +   self.phase0);

	def __init__(self, x, y, z, amplitude = 1, frequency = 1, phase0 = 0):
		self.x = x;
		self.y = y;
		self.z = z;
		
		self.amplitude = amplitude;
		self.frequency = frequency;
		self.phase0 = phase0;

		
