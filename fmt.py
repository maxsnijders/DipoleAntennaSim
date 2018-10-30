from __future__ import division;
import model;
import harmoniclinearsource as hls;
import squarelinearsource as sls;
import amlinearsource as als;
import antenna as ant;
import settings;
import numpy as np;
import signals as sig;
import output as out;
import dipoleantenna as diant;
import math;
import matplotlib.pyplot as plt;
import directivityplot as dp;
import antennaconfiguration as AC;
import harmoniccircularsource as hcs;
import harmonicrandomsource as hrs;
import os;

Frequency = settings.default_freq;
Wavelength = sig.frequency_to_wavelength(Frequency);
'''
os.system("python demo_fft.py");

print "Processing: Antenna reception of noise/signal";
#Linear Harmonic Source
Source = hls.HarmonicLinearSource(0, 0, Wavelength * 1E9, 1, Frequency);
SourceNoise = hls.HarmonicLinearSource(0, Wavelength * 1E9, 0, 1, Frequency * 7);
model.model_antenna_signal_noise(Frequency, Source, SourceNoise, "Linear[Harmonic]-Linear[Harmonic]");
#Circular Harmonic Source
Source = hcs.HarmonicCircularSource(0, 0, Wavelength * 1E9, 1, Frequency);
SourceNoise = hcs.HarmonicCircularSource(0, Wavelength * 1E9, 0, 1, Frequency * 7);
model.model_antenna_signal_noise(Frequency, Source, SourceNoise, "Circular[Harmonic]-Circular[Harmonic]");
#Random-polarisation Harmonic Source
Source = hrs.HarmonicRandomSource(0, 0, Wavelength * 1E9, 1, Frequency);
SourceNoise = hrs.HarmonicRandomSource(0, Wavelength * 1E9, 0, 1, Frequency * 7);
model.model_antenna_signal_noise(Frequency, Source, SourceNoise, "Random[Harmonic]-Random[Harmonic]");
#Square - linear
Source = sls.SquareLinearSource(0, 0, Wavelength * 1E9, 1, Frequency);
SourceNoise = sls.SquareLinearSource(0, Wavelength * 1E9, 0, 1, Frequency * 7);
model.model_antenna_signal_noise(Frequency, Source, SourceNoise, "Linear[Square]-Linear[Square]");
#Random source, linear noise
Source = hrs.HarmonicRandomSource(0, 0, Wavelength * 1E9, 1, Frequency);
SourceNoise = hls.HarmonicLinearSource(0, Wavelength * 1E9, 0, 1, Frequency * 7);
model.model_antenna_signal_noise(Frequency, Source, SourceNoise, "Random[Harmonic]-Linear[Harmonic]");
'''

#Model signal strength based on angle of source moving in yz plane with antenna in xy plane with antenna wires oriented in the x direction.
print "Processing: Directivity plot in 2D planes";
#Perpendicular to the antennae
A1 = diant.DipoleAntenna(0, 0, 			 	0, Wavelength/2, 0, 			0);
A2 = diant.DipoleAntenna(0, Wavelength/2, 	0, Wavelength/2, Wavelength/2, 	0);
Antennae = AC.AntennaConfiguration([A1, A2], (lambda Signals: (Signals[0] + Signals[1])/2));
Angles, SignalStrengths = model.signal_strength_angle_out_of_plane(Antennae, Frequency);
dp.directivityplot(Angles, SignalStrengths, "Directivity of Dual Dipole Antenna in plane perpendicular to antennae", "directivity_perpendicular_dualdipole");

A1 = diant.DipoleAntenna(0, 0, 			 	0, Wavelength/2, 0, 			0);
Antennae = AC.AntennaConfiguration([A1], (lambda Signals: Signals[0]));
Angles, SignalStrengths = model.signal_strength_angle_out_of_plane(Antennae, Frequency);
dp.directivityplot(Angles, SignalStrengths, "Directivity of Single Dipole Antenna in plane perpendicular to antennae", "directivity_perpendicular_singledipole");

A1 = diant.DipoleAntenna(0, 0, 0, 0, Wavelength/2,0);
A2 = diant.DipoleAntenna(Wavelength/2, 0, 	0, Wavelength/2, Wavelength/2, 	0);
Antennae = AC.AntennaConfiguration([A1, A2], (lambda Signals: (Signals[0] + Signals[1])/2));
Angles, SignalStrengths = model.signal_strength_angle_out_of_plane(Antennae, Frequency);
dp.directivityplot(Angles, SignalStrengths, "Directivity of Dual Dipole Antenna in plane parallel to antennae", "directivity_parallel_dualdipole", "X");

#Parallel to the antenna
A1 = diant.DipoleAntenna(0, 0, 0, 0, Wavelength/2,	0);
Antennae = AC.AntennaConfiguration([A1], (lambda Signals: Signals[0]));
Angles, SignalStrengths = model.signal_strength_angle_out_of_plane(Antennae, Frequency);
dp.directivityplot(Angles, SignalStrengths, "Directivity of Single Dipole Antenna in plane parallel to antennae", "directivity_parallel_singledipole", "X");

'''
print "Processing: 3D Directivity plot for dual dipole"
#Standard Dual Dipole
A1 = diant.DipoleAntenna(0, 0, 			 	0, Wavelength/2, 0, 			0);
A2 = diant.DipoleAntenna(0, Wavelength/2, 	0, Wavelength/2, Wavelength/2, 	0);
Antennae = AC.AntennaConfiguration([A1, A2], (lambda Signals: (Signals[0] + Signals[1])/2));
AnglesPhi, AnglesTheta, SignalStrengths = model.signal_strength_all_directions(Antennae, Frequency);
dp.directivityplotomnidirectional(AnglesPhi, AnglesTheta, SignalStrengths, "Directivity of Dual-Dipole Antenna", "Omnidirectional-Directivity-Dual-Dipole");

print "Processing: 3D Directivity plot for single monopole";
#Single Dipole
A1 = diant.DipoleAntenna(0, 0, 0, Wavelength/2, 0, 0);
Antennae = AC.AntennaConfiguration([A1], (lambda Signals: Signals[0]));
AnglesPhi, AnglesTheta, SignalStrengths = model.signal_strength_all_directions(Antennae, Frequency);
dp.directivityplotomnidirectional(AnglesPhi, AnglesTheta, SignalStrengths, "Omnidirectional Directivity Single Dipole", "Omnidirectional-Directivity-Single-Dipole");

print "Processing: 3D Directivity plot for quad-dipole"
A1 = diant.DipoleAntenna(0, 0, 0, Wavelength/2, 0, 0);
A2 = diant.DipoleAntenna(0, Wavelength/2, 0, Wavelength/2, Wavelength/2, 0);
A3 = diant.DipoleAntenna(0, 0, Wavelength/2, 0, Wavelength/2, Wavelength/2);
A4 = diant.DipoleAntenna(Wavelength/2, 0, Wavelength/2, Wavelength/2, Wavelength/2, Wavelength/2);
Antennae = AC.AntennaConfiguration([A1,A2,A3,A4], (lambda S: ((S[0] + S[1])/2 - (S[2] + S[3]/2))/2));
AnglesPhi, AnglesTheta, SignalStrengths = model.signal_strength_all_directions(Antennae, Frequency);
dp.directivityplotomnidirectional(AnglesPhi, AnglesTheta, SignalStrengths, "Omnidirectional Directivity Quad-Dipole", "Omnidirectional-Directivity-quad-Dipole");
#Model signal-to-noise-ratio dependance of noise frequency.

print "Processing: Frequency of noise dependance of signal/noise ratio for dual dipole"
A1 = diant.DipoleAntenna(0, 0, 			 	0, Wavelength/2, 0, 			0);
A2 = diant.DipoleAntenna(0, Wavelength/2, 	0, Wavelength/2, Wavelength/2, 	0);
Antennae = AC.AntennaConfiguration([A1, A2], (lambda Signals: (Signals[0] + Signals[1])/2));
Frequencies, SignalToNoiseRatios = model.signal_to_noise_noise_freq(Antennae, Frequency);
out.plot_signal_noise_ratio_frequency(SignalToNoiseRatios, Frequencies, "Signal/Noise ratio versus Noise Frequency for Dual Dipole", "Signal-To-Noise-Ratio-Noise-Frequency-Dual-Dipole");

print "Processing: Frequency of noise dependance of signal/noise ratio for single dipole";
A1 = diant.DipoleAntenna(0, 0, 			 	0, Wavelength/2, 0, 			0);
Antennae = AC.AntennaConfiguration([A1], (lambda Signals: Signals[0]));
Frequencies, SignalToNoiseRatios = model.signal_to_noise_noise_freq(Antennae, Frequency);
out.plot_signal_noise_ratio_frequency(SignalToNoiseRatios, Frequencies, "Signal/Noise ratio versus Noise Frequency for single Dipole", "Signal-To-Noise-Ratio-Noise-Frequency-Single-Dipole");

print "Processing: Signal strength dependancy on antenna spacing";
Frequencies, SignalStrengths = model.signal_strength_antenna_spacing();
fig4 = plt.figure();
ax4 = fig4.add_subplot(111);
ax4.plot(Frequencies, SignalStrengths);
ax4.set_xlabel("Antenna Spacing/length [Normalised: 1 :  $\lambda$ = Antenna Spacing/Length]");
ax4.set_ylabel("Signal Strength [Normalised]");
ax4.set_title("Signal Strength for dual dipole antenna verses source frequency");
ax4.set_ylim([0, 1]);
fig4.savefig("Output/Signal-Strength-Relative-Source-Frequency.png");
plt.close(fig4);


A1 = diant.DipoleAntenna(0, 0, 			 	0, Wavelength/2, 0, 			0);
A2 = diant.DipoleAntenna(0, Wavelength/2, 	0, Wavelength/2, Wavelength/2, 	0);
Antennae = AC.AntennaConfiguration([A1, A2], (lambda Signals: (Signals[0] + Signals[1])/2));
#Frequencies = np.linspace(Frequency/10, Frequency*10, 10);
Frequencies = np.array([1/8, 1/6, 1/4, 1/3, 1/2, 3/4, 1, 1.25, 1.5, 2]) * Frequency;
AnglesPhi, AnglesTheta, SignalStrengths, Frequencies = model.signal_strengths_all_directions_frequencies(Antennae, Frequencies);
Frequencies /= Frequency;
dp.directivityplotomnidirectionalperfrequency(AnglesPhi, AnglesTheta, SignalStrengths, Frequencies, "Directivity plot", "freq-dep-dir-plot");
'''

