from scipy import fft, arange;
from scipy import fftpack as fftp;
import numpy as np;

#Function that returns the fourier-transformed signal components from a given signal.
#Returns a list of frequencies (real numbers) and the amplitudes of the oscillations (complex)
#Reconstruction of signal: signal = Sum over Each Signal: ((e^(i * freq * 2pi * time) * amp).real);
def fourier_transform(signal, total_time):
	N = len(signal);
	sample_rate = total_time / N;
	
	#Take only the one sided frequency range
	frq = fftp.fftfreq(N, sample_rate);
	frq = frq[range(N/2)];
	Y = fft(signal) / N;
	Y = 2 * Y[range(N/2)];
	Y[0] /= 2;
	return frq, Y;
