import antenna
import numpy as np;
import constants as const;
import math
import geometry as geo;
import signals as sig;
import fft;
import matplotlib.pyplot as plt;
import output as out;

class DipoleAntenna(antenna.Antenna):
	#Position for the first tip
	x1 = 0;
	y1 = 0;
	z1 = 0;
	
	#Position for the second tip
	x2 = 1;
	y2 = 0;
	z2 = 0;
			
	def __init__(self, x1, y1, z1, x2, y2, z2):
		self.x1 = x1;
		self.y1 = y1;
		self.z1 = z1;
		
		self.x2 = x2;
		self.y2 = y2;
		self.z2 = z2;
				
	def calculate_signal(self, Source, Time):
		#Find the midpoint of the antenna
		MidX = (self.x1 + self.x2)/2;
		MidY = (self.y1 + self.y2)/2;
		MidZ = (self.z1 + self.z2)/2;
		
		#We want to know the length of the antenna
		Length      			= geo.distance_cartesian(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2);
		HalfLength				= Length / 2;
		
		#We want to know how much of the incoming E wave is perpendicular to the antenna.
		DotProductOfVectors = (self.x2 - self.x1) * (Source.x  - MidX) + (self.y2 - self.y1) * (Source.y - MidY) + (self.z2 - self.z1) * (Source.z - MidZ);
		SourceDistance		= geo.distance_cartesian(Source.x, Source.y, Source.z, MidX, MidY, MidZ);
		CosAngle			= DotProductOfVectors / (Length * SourceDistance);
		SinAngle			= np.sqrt(1 - CosAngle**2);
		
		#Look up the signal sent at t' = (t - d/c)
		travel_time 			= sig.signal_travel_time(SourceDistance);
		Source_Signal			= Source.signal(Time - travel_time);
		Signal_Duration			= max(Time) - min(Time);
		Frequencies, Amplitudes = fft.fourier_transform(Source_Signal, Signal_Duration);

		#Now construct the signal on the antenna terminals
		signal = np.zeros(len(Time));
		for i in np.arange(0, len(Frequencies), 1):
			#Unpack FFT transformed data
			Frequency 	= Frequencies[i];
			Amplitude 	= Amplitudes[i];
			Wavenumber 	= Frequency * 2 * math.pi  / const.c; #w / c == 2 * pi * f / c

			#Voltage across the terminals of a receiving antenna
			#Kirk T. McDonald, Joseph Henry Laboratories, Princeton University, Princeton NJ 08544
			if(np.sin(Wavenumber * HalfLength) == 0):
				continue;
			
			#What part of the wave hits at a perpendicular angle
			PerpendicularPart	= np.cos(Source.polarisation(Time - travel_time)) * SinAngle;
			
			#What's the E-field at that time?
			E0 					= PerpendicularPart * Amplitude * np.exp(1.j * Frequency * math.pi * Time); #@TODO: Factor 2???;
			Potential 			= - 2 * E0 / Wavenumber * (1 - np.cos(Wavenumber * HalfLength)) / np.sin(Wavenumber * HalfLength);
			signal 	   	        += Potential.real;
			
		return signal;
