import numpy as np
import matplotlib.pyplot as plt
import math;

def plot_signal(Time, Amplitude, Title, Filename):
	fig1 = plt.figure();
	ax1 = fig1.add_subplot(111);
	ax1.plot(Time, Amplitude);
	ax1.set_title(Title);
	ax1.set_xlabel("Time [s]");
	ax1.set_ylabel("Signal");
	ax1.grid(True);
	
	limits = np.array(ax1.get_ylim());
	if(abs(limits[1]) > abs(limits[0])):
		limits[0] = -1 * limits[1];
	else:
		limits[1] = -1 * limits[0];
		
	ax1.set_ylim(limits);
	
	filename = "Output/{fn}.png".format(fn = Filename);
	fig1.savefig(filename);

def plot_signal_noise_ratio_frequency(SignalToNoiseRatios, Frequencies, Title, FName):
	fig3 = plt.figure();
	ax3 = fig3.add_subplot(111);

	for k in np.arange(0, max(Frequencies) / 2, 1):
		if(k < 1):
			ax3.axvline(2*k + 1, color="red", label="2k+1", zorder=2);
		else:
			ax3.axvline(2*k +1, color="red", zorder=2);
		
	ax3.plot(Frequencies, SignalToNoiseRatios, label="Signal/Noise Ratio", zorder=1);
	ax3.legend(loc=1);
	ax3.set_xlabel("Frequency [Normalised: $\lambda$ = Antenna Length]");
	ax3.set_ylabel("Signal To Noise Ratio");
	ax3.set_title(Title);
	ax3.set_ylim([0, 10]);

	fig3.savefig("Output/{FN}.png".format(FN = FName));
	plt.close(fig3);

def round_sig(number, significantfigures):
	x = number;
	n = significantfigures;
	
	return round(x, int(n - math.ceil(math.log10(abs(x)))));
