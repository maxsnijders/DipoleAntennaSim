import numpy as np;

class AntennaConfiguration:
	Antennae = [];
	SignalProcessFunction = None;
	
	def __init__(self, Antennae, SignalProcessFunction):
		self.Antennae = Antennae;
		self.SignalProcessFunction = SignalProcessFunction;
		
	def calculate_signal(self, Source, Time):
		Signals = np.zeros((len(self.Antennae), len(Time)));
		
		for i in np.arange(0, len(self.Antennae), 1):
			Antenna = self.Antennae[i];
			Signal = Antenna.calculate_signal(Source, Time);
			Signals[i] = Signal;
			
		return self.SignalProcessFunction(Signals);
