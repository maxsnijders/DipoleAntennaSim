#Interface file
import numpy as np;
import fft;
import math;
import scipy;
import matplotlib.pyplot as plt;

from scipy import signal as scipy_sig;

def plot_for_signal(time, signal, name):
	fig1 = plt.figure();
	ax1 = fig1.add_subplot(111);
	ax1.plot(time, signal);
	ax1.set_title("Generated Signal ({n})".format(n = name));
	ax1.set_xlabel("Time [seconds]");
	ax1.set_ylabel("Amplitude");
	ax1.grid(True);

		
	Frequencies, Amplitudes = fft.fourier_transform(signal, max(time));
	fig2 = plt.figure();
	ax2 = fig2.add_subplot(111);
	ax2.plot(Frequencies, Amplitudes.real, label="Real part");
	ax2.plot(Frequencies, Amplitudes.imag, label="Imag part");
	ax2.set_title("Frequency Components ({n})".format(n = name));
	ax2.set_xlabel("Frequency [Hz]");
	ax2.set_ylabel("Amplitude");
	ax2.legend(loc = 1);
	ax2.grid(True);
	fig2.savefig("Output/FFT_Demo/{n}_fft.png".format(n = name));
	plt.close(fig2);
	
	fig4 = plt.figure();
	ax4 = fig4.add_subplot(111);
	
	signal_rebuilt = np.zeros(len(time));
	
	for i in np.arange(0, len(Frequencies)):
		freq = Frequencies[i];
		amp  = Amplitudes[i];
		
		comp_signal = np.exp(1j * freq * 2 * math.pi * time) * amp;
		comp_signal = comp_signal.real; #Because the world is real...
		signal_rebuilt += comp_signal;
		
		if(i == 0):
			ax4.plot(time, comp_signal, c="green", label="Signal Components");
		else:
			ax4.plot(time, comp_signal, c="green");
			
	ax4.grid(True);
	ax4.plot(time, signal, c="blue", label="Original Signal");
	ax4.legend(loc = 1);
	ax4.set_xlabel("Time [seconds]");
	ax4.set_ylabel("Amplitude");
	ax4.set_title("Signal components / Total Signal");
	fig4.savefig("Output/FFT_Demo/{n}_components.png".format(n = name));
	
	fig3 = plt.figure();
	ax3 = fig3.add_subplot(111);
	ax3.plot(time, signal_rebuilt);
	ax3.grid(True);
	ax3.set_title("Rebuilt Signal ({n})".format(n = name));
	ax3.set_xlabel("Time [seconds]");
	ax3.set_ylabel("Amplitude");
	fig3.savefig("Output/FFT_Demo/{n}_rebuilt.png".format(n = name));
	ylim = ax3.get_ylim();
	ax1.set_ylim(ylim);
	fig1.savefig("Output/FFT_Demo/{n}_signal.png".format(n = name));
	plt.close(fig1);
	plt.close(fig3);
	
print "Processing: FFT Demo plots"
time = np.linspace(0, 10, 1E4);

signal = scipy_sig.square(2 * math.pi * time);
plot_for_signal(time, signal, "Square");
signal = scipy_sig.sawtooth(2 * math.pi * time);
plot_for_signal(time, signal, "Sawtooth");
signal = 3 * np.sin(2 * math.pi * time) + 2 * np.cos(math.pi * time) + np.sin(7 * math.pi * time);
plot_for_signal(time, signal, "Sines+cosines");
signal =  scipy_sig.square(math.pi * time) + 1.123;
plot_for_signal(time, signal, "Square-translated");
