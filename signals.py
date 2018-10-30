import geometry as geo;
import constants as const;
import numpy as np;

def signal_travel_time(distance):
	return distance / const.c;

def frequency_to_wavelength(freq):
	return const.c / freq;

def signal_to_noise_ratio(Signal, SignalWithNoise):
	Noise = SignalWithNoise - Signal;
	
	Indices 	= np.nonzero(Noise);
	AllIndices 	= np.arange(0, len(Signal), 1);
	
	SignalToNoiseRatio = np.zeros(len(Signal));
	
	for i in Indices:
		SignalToNoiseRatio[i] = abs(Signal[i] / Noise[i]); 	
		
	return np.average(SignalToNoiseRatio);
	
	
