#Main model python file

#Our own files
import geometry as geo;
import antenna as ant;
import source as src;
import constants as const;
import harmoniclinearsource as hls;
import squarelinearsource as sls;
import signals as sig;
import settings;
import dipoleantenna as diant;
import output as out;
import itertools

#System files
import math;
import numpy as np;

#Function to calculate the signal on an antenna "Antenna", source "Source" for times Time (which is an array of times in seconds)
def calc_signal_antenna(Antenna, Source, Time):
	return Antenna.calculate_signal(Source, Time);

#Simulate the signal to noise ratio for varying noise frequencies (noise in the plane of the antenna).
def signal_to_noise_noise_freq(Antennae, Frequency):
	Wavelength = sig.frequency_to_wavelength(Frequency);
	
	Times = np.linspace(0, 10 / Frequency, settings.timesteps);

	Source = hls.HarmonicLinearSource(0, 0, Wavelength * 1E13, 1, Frequency);
	
	Signal = Antennae.calculate_signal(Source, Times);
	
	Frequencies 		= np.linspace(Frequency / 10, Frequency * 10, 10000);
	SignalNoiseRatios	= np.zeros(len(Frequencies));
	
	for i in np.arange(0, len(Frequencies), 1):
		NoiseFreq	= Frequencies[i];
		NoiseSource = hls.HarmonicLinearSource(0, Wavelength * 1E10, 0, 1,  NoiseFreq);
		
		Noise = Antennae.calculate_signal(NoiseSource, Times);
		SignalWithNoise = Signal + Noise;
		
		SignalToNoiseRatio 	 = sig.signal_to_noise_ratio(Signal, SignalWithNoise);
		
		SignalNoiseRatios[i]= SignalToNoiseRatio;
		
		del NoiseSource;

	return Frequencies / Frequency, SignalNoiseRatios;

def signal_strength_angle_out_of_plane(Antennae, Frequency):
	
	Angles = np.linspace(0, 2 * math.pi, settings.angles_steps);
	SignalStrengths = np.zeros(len(Angles));
	
	Wavelength = sig.frequency_to_wavelength(Frequency);

	#A1 = diant.DipoleAntenna(0, 0, 				0, Wavelength / 2, 0, 			  0);
	#A2 = diant.DipoleAntenna(0, Wavelength / 2, 0, Wavelength / 2, Wavelength / 2, 0);	
	
	Distance = 1E10 * Wavelength;
	
	Times = np.linspace(0, 10/Frequency, settings.timesteps)
	
	for i in np.arange(0, len(Angles), 1):
		Angle  = Angles[i];
		Source = hls.HarmonicLinearSource(0, Distance * np.cos(Angle), Distance * np.sin(Angle), 1, Frequency);
		
		Signal = Antennae.calculate_signal(Source, Times);
		
		SignalStrength 		= max(Signal);
		SignalStrengths[i]  = SignalStrength;

		del Source;

	return Angles, SignalStrengths / max(SignalStrengths);

def signal_strength_all_directions(Antennae, Frequency):
	AnglesPhi 	= np.linspace(0, 2 * math.pi, settings.angles_steps);
	AnglesTheta = np.linspace(0, math.pi, settings.angles_steps);
	
	AnglesPhi, AnglesTheta = np.meshgrid(AnglesPhi, AnglesTheta);  

	SignalStrengths = np.zeros((len(AnglesPhi),len(AnglesTheta)));
	
	Wavelength 	= sig.frequency_to_wavelength(Frequency);
	Distance 	= 1E10 * Wavelength; #Far-field source
	Times 		= np.linspace(0, 1/Frequency, settings.timesteps);
	
	#A1 = diant.DipoleAntenna(0, 0, 			 	0, Wavelength/2, 0, 			0);
	#A2 = diant.DipoleAntenna(0, Wavelength/2, 	0, Wavelength/2, Wavelength/2, 	0);

	for i in np.arange(0, len(AnglesPhi)):
		print "\rCalculating: {i}/{n}".format(i = i+1, n = len(AnglesPhi));
		for j in np.arange(0, len(AnglesTheta)):
			AnglePhi 	= AnglesPhi[i,j];
			AngleTheta	= AnglesTheta[i,j];
				
			Source = hls.HarmonicLinearSource(	Distance * np.sin(AngleTheta) * np.cos(AnglePhi),
												Distance * np.sin(AngleTheta) * np.sin(AnglePhi),
												Distance * np.cos(AngleTheta), 1, Frequency);
											
			Signal = Antennae.calculate_signal(Source, Times);
				
			SignalStrength			= max(Signal);
			SignalStrengths[i,j] 	= SignalStrength;
	
	print "";
	if(np.max(np.max(SignalStrengths, 1)) == 0):
		return AnglesPhi, AnglesTheta, np.zeros((len(AnglesPhi), len(AnglesTheta)));
			
	return AnglesPhi, AnglesTheta, SignalStrengths / np.max(np.max(SignalStrengths, 1));	

def signal_strengths_all_directions_frequencies(Antennae, Frequencies):
	AnglesPhi 		= [];
	AnglesTheta 	= [];
	SignalStrengths = [];
	
	for i in np.arange(0, len(Frequencies), 1):
		Frequency = Frequencies[i];
		print "Freq = {f}. [{F}/{T}]".format(f = Frequency, F = i+1, T = len(Frequencies));
		AnglesPhiPerF, AnglesThetaPerF, SignalStrengthsPerF = signal_strength_all_directions(Antennae, Frequency);
		AnglesPhi.append(AnglesPhiPerF);
		AnglesTheta.append(AnglesThetaPerF);
		SignalStrengths.append(SignalStrengthsPerF);
	
	return AnglesPhi, AnglesTheta, SignalStrengths, Frequencies;

def model_antenna_signal_noise(Frequency, Source, SourceNoise, Title):
	Wavelength = sig.frequency_to_wavelength(Frequency);
	Time = np.linspace(0, 5/Frequency, 1000);
	
	A1 = diant.DipoleAntenna(0, 0, 0, Wavelength/2, 0, 0);
	A2 = diant.DipoleAntenna(0, Wavelength/2, 0, Wavelength/2, Wavelength/2, 0);
	
	#Signal from the first source on the first antenna
	
	Signal1 = calc_signal_antenna(A1, Source, Time);
	NormFactor = max(Signal1);
	if(NormFactor == 0):
		print "This system has no signal";
		return;
		
	out.plot_signal(Time, Signal1 / NormFactor, "Single Dipole [noiseless] {T}".format(T = Title), "{T}_sig_single_dipole_pure".format(T = Title));
		
	Signal_noise = calc_signal_antenna(A1, SourceNoise, Time);
	out.plot_signal(Time, Signal_noise / NormFactor, "Single Dipole [just noise] {T}".format(T = Title), "{T}_sig_single_dipole_justnoise".format(T = Title));
	
	Signal1_t = Signal1 + Signal_noise;
	out.plot_signal(Time, Signal1_t / NormFactor, "Single Dipole [first, with noise] {T}".format(T = Title), "{T}_sig_single_dipole_noise_1".format(T = Title));
	
	Signal2 = calc_signal_antenna(A2, Source, Time);
	Signal_noise_2 = calc_signal_antenna(A2, SourceNoise, Time);
	Signal2_t = Signal2 + Signal_noise_2;
	
	out.plot_signal(Time, Signal2_t / NormFactor, "Single  Dipole [second, with noise] {T}".format(T = Title), "{T}_sig_single_dipole_noise_2".format(T = Title));
	
	Signalt = (Signal1_t + Signal2_t)/2;
	out.plot_signal(Time, Signalt / NormFactor, "Dual Dipole [raw] {T}".format(T = Title), "{T}_sig_double_dipole_noise".format(T = Title));
		
def signal_strength_antenna_spacing():
	Frequency 	= settings.default_freq;
	Wavelength	= sig.frequency_to_wavelength(Frequency);
	
	Source 		= hls.HarmonicLinearSource(0, 0, Wavelength * 1E9, 1, Frequency);
	
	Frequencies 	= np.linspace(Frequency / 2, Frequency * 10, 100);
	SignalStrengths = np.zeros(len(Frequencies));

	for i in np.arange(0, len(Frequencies), 1):
		Freq		= Frequencies[i];
		Times 		= np.linspace(0, 2/Freq, 100);
		Wavelength	= sig.frequency_to_wavelength(Freq);
		
		A1 			= diant.DipoleAntenna(0, 0, 			0, Wavelength/2, 0, 			0);
		A2 			= diant.DipoleAntenna(0, Wavelength/2, 	0, Wavelength/2, Wavelength/2, 	0);
		
		Signal1 	= calc_signal_antenna(A1, Source, Times);
		Signal2 	= calc_signal_antenna(A2, Source, Times);
		
		Total_Signal = (Signal1 + Signal2) / 2;
		SignalStrengths[i] = max(Total_Signal);
	
	return Frequencies, (SignalStrengths / max(SignalStrengths));
