#Signal point source
class Source:
	x = 0;
	y = 0;
	z = 0;
	
	#Signal at time t, should return a number meaning its amplitude
	signal = None;
	
	#Polarisation at time t, should return a number meaning the angle of polarisation
	polarisation = None;
