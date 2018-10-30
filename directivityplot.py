from __future__ import division;
import numpy as np;
import matplotlib.pyplot as plt;
from mpl_toolkits.mplot3d import Axes3D
import os;
import math;
from matplotlib import cm
import settings as sett
import output as out;

def directivityplot(angles, signalstrengths, title, fname, horlabel="Y", vlabel="Z"):	
	x = signalstrengths*np.cos(angles)
	y = signalstrengths*np.sin(angles)
	
	fig = plt.figure();
	ax = fig.add_subplot(111);
	ax.plot(x, y);
	ax.set_xlabel(horlabel);
	ax.set_ylabel(vlabel);
	ax.set_title(title);
	ax.set_aspect('equal');
	ax.grid(True);
	ax.axhline(0, color='black')
	ax.axvline(0, color='black')
	
	xlim = ax.get_xlim();
	ylim = ax.get_ylim();
	
	if(max(xlim) - min(xlim) >= max(ylim) - min(ylim)):
		ax.set_ylim(xlim);
	else:
		ax.set_xlim(ylim);
			
	fig.savefig("Output/{fn}.png".format(fn = fname));
	plt.close(fig);
	
def directivityplotomnidirectional(AnglesPhi, AnglesTheta, SignalStrengths, Title, FName):
	x = SignalStrengths*np.sin(AnglesTheta)*np.cos(AnglesPhi)
	y = SignalStrengths*np.sin(AnglesTheta)*np.sin(AnglesPhi)
	z = SignalStrengths*np.cos(AnglesTheta)
	
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	surface = ax.plot_surface(x, y, z, rstride=5, cstride=5, cmap=cm.jet, linewidth=1, antialiased=True, shade=True)
	fig.colorbar(surface)
	ax.set_xlabel("X");
	ax.set_ylabel("Y");
	ax.set_zlabel("Z");
	ax.set_title(Title);
	ax.set_aspect('equal');
	ax.grid(True);
	
	xlim = ax.get_xlim();
	ylim = ax.get_ylim();
	zlim = ax.get_zlim();
	
	if((max(xlim) - min(xlim)) >= (max(ylim) - min(ylim)) and (max(xlim) - min(xlim)) >= (max(zlim) - min(zlim))):
		ax.set_ylim(xlim);
		ax.set_zlim(xlim);
	elif((max(ylim) - min(ylim)) >= (max(xlim) - min(xlim)) and (max(ylim) - min(ylim)) >= (max(zlim) - min(zlim))):
		ax.set_xlim(ylim);
		ax.set_zlim(ylim);
	else:
		ax.set_xlim(zlim);
		ax.set_ylim(zlim);
	
	TotalDuration = 20;
	FrameRate 	= 25;
	timelapse 	= np.linspace(0,1,TotalDuration*FrameRate)
	angles 		= np.linspace(0,360,len(timelapse));
	elevation 	= timelapse * 20 - 10;
	zoom 		= timelapse * 2 + 1;
		
	xlimits = np.array(ax.get_xlim());
	ylimits = np.array(ax.get_ylim());
	zlimits = np.array(ax.get_zlim());
	
	print "";
	for i in np.arange(0, len(timelapse), 1):
		print "\rDrawing: {i}/{n}".format(i = i+1, n = len(timelapse));
		ax.set_ylim(1.0/zoom[i] * np.array(ylimits));
		ax.set_xlim(1.0/zoom[i] * np.array(xlimits));
		ax.set_zlim(1.0/zoom[i] * np.array(zlimits));
		ax.view_init(elev=elevation[i], azim=angles[i])
		number = "%05d"% i;
		fig.savefig("Output/3DDirectivity/movie_{t}_{n}.png".format(t=FName, n=number));
		
	print "";
	print "Stitching it into a video...";
	#fig.savefig("Output/{fn}.png".format(fn = FName));
	plt.close(fig);
	os.system("rm Output/{FN}.mkv".format(FN = FName));
	os.system("ffmpeg -r {r} -f image2 -i Output/3DDirectivity/movie_{t}_%05d.png -c:v libx264 -preset ultrafast -qp 0 Output/{FN}.mkv".format(t=FName, FN = FName, r = FrameRate));
	#os.system("rm Output/3DDirectivity/*.png");

def directivityplotomnidirectionalperfrequency(AnglesPhi, AnglesTheta, SignalStrengths, Frequencies, Title, FName):
	ForwardTimeProgression = True;
	for j in np.arange(0, len(Frequencies)):
		Frequency = Frequencies[j];
		
		AnglesPhiforF = AnglesPhi[j]
		AnglesThetaforF = AnglesTheta[j]
		SignalStrengthsforF = SignalStrengths[j]
	
		x = SignalStrengthsforF*np.sin(AnglesThetaforF)*np.cos(AnglesPhiforF)
		y = SignalStrengthsforF*np.sin(AnglesThetaforF)*np.sin(AnglesPhiforF)
		z = SignalStrengthsforF*np.cos(AnglesThetaforF)
	
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		surface = ax.plot_surface(x, y, z, rstride=5, cstride=5, cmap=cm.jet, linewidth=1, antialiased=True, shade=True)
		fig.colorbar(surface)
		ax.set_xlabel("X");
		ax.set_ylabel("Y");
		ax.set_zlabel("Z");
		ax.set_title(Title + " for norm. freq. = " + str(out.round_sig(Frequency, 4)));
		ax.set_aspect('equal');
		ax.grid(True);
		
		xlim = ax.get_xlim();
		ylim = ax.get_ylim();
		zlim = ax.get_zlim();
		
		if((max(xlim) - min(xlim)) >= (max(ylim) - min(ylim)) and (max(xlim) - min(xlim)) >= (max(zlim) - min(zlim))):
			ax.set_ylim(xlim);
			ax.set_zlim(xlim);
		elif((max(ylim) - min(ylim)) >= (max(xlim) - min(xlim)) and (max(ylim) - min(ylim)) >= (max(zlim) - min(zlim))):
			ax.set_xlim(ylim);
			ax.set_zlim(ylim);
		else:
			ax.set_xlim(zlim);
			ax.set_ylim(zlim);
		
		#Settings
		TotalDuration = 3;
		FrameRate 	= 25;
		timelapse 	= np.linspace(0,1,TotalDuration*FrameRate)
		angles 		= np.linspace(0,120,len(timelapse));
		elevation 	= timelapse * 10;
		zoom 		= timelapse * 0.5 + 1;
			
		xlimits = np.array(ax.get_xlim());
		ylimits = np.array(ax.get_ylim());
		zlimits = np.array(ax.get_zlim());
	
		TimeProgression = np.arange(0, len(timelapse), 1)
		FrameIndices = np.arange(0, len(timelapse), 1);
		if (ForwardTimeProgression == False):
			TimeProgression = len(timelapse) - TimeProgression - 1;
			FrameIndices = len(FrameIndices) - FrameIndices  - 1;
				
		for i in TimeProgression:
			FrameIndex = FrameIndices[i];
			ax.set_ylim(1.0/zoom[i] * np.array(ylimits));
			ax.set_xlim(1.0/zoom[i] * np.array(xlimits));
			ax.set_zlim(1.0/zoom[i] * np.array(zlimits));
			ax.view_init(elev=elevation[i], azim=angles[i])
			
			FrameNumber = int(FrameIndex + j * len(FrameIndices));
			number = "%07d" % FrameNumber;
			print "Generating frame nr. {n}/{t}".format(n = number, t = len(Frequencies) * len(FrameIndices));
			fig.savefig("Output/3DDirectivity/movie_{t}_{n}.png".format(t=FName, n=number));
			
		#fig.savefig("Output/{fn}.png".format(fn = FName));
		plt.close(fig);
		ForwardTimeProgression = not ForwardTimeProgression;
	
	print "Stitching it into a video...";
	os.system("rm Output/{FN}.mkv".format(FN = FName));
	os.system("ffmpeg -r {r} -f image2 -i Output/3DDirectivity/movie_{t}_%07d.png -c:v libx264 -preset ultrafast -qp 0 Output/{FN}.mkv".format(t=FName, FN = FName, r = FrameRate));
		#os.system("rm Output/3DDirectivity/*.png");
		
	
