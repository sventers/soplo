
import os

import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft
import wave
import tensorflow as tf

import glob

prefix_dir = 'EMOVO/'
indirs = ['f1','f2','f3','m1','m2','m3']
indirs = [  prefix_dir+s     for s in indirs  ]



# create index array of file names of files
def get_filename_and_location_index (dirs_in):
	filepaths = []
	for root, dirs, filenames in os.walk(dirs_in):
		for f in filenames:
			filepaths.append(root+'/'+f)
	# the first filepath is a hidden directory. see alternate
	return filepaths[1:]

def alternate_get_filename_and_location_index (directory):
	return glob.glob(directory+'/*/*.wav')


# convert wave file to fft
def get_fft_from_filename_of_wave (myAudio):
	samplingFreq, wav_buff = wavfile.read(myAudio)
	wav_buff = wav_buff / (2.**14)  #32 bit
	samplePoints = float(wav_buff.shape[0])
	signalDuration = wav_buff.shape[0] / samplingFreq
	

	channelone = wav_buff[:,0]
	channeltwo = wav_buff[:,1]


	timeArray = np.arange(0, samplePoints, 1)
	timeArray = timeArray / samplingFreq
	timeArray = timeArray * 1000
	print('this is about to plot')
	return timeArray, channelone, channeltwo
	#plt.plot(timeArray, channelone, color='B')
	#plt.show()
	

# graph individual fft
def graph_wav():
	from bokeh.plotting import figure, show, output_file
	t, a, b = get_fft_from_filename_of_wave(filepaths[0])
	
	p = figure(title='wavform example')

	

	p.multi_line(np.array_split(a, 1), np.array_split(t,1), line_color='#C6DBEF', line_alpha=.8, line_width=1.5)
	output_file('wavform.html', title='wavform.py example')
	show(p)

# graph sum of ffts
def graph_summed_fft():
	t, a, b = get_fft_from_filename_of_wave(filepaths[0])
	from bokeh.layouts import row, column
	from bokeh.models import BoxSelectTool, LassoSelectTool, Spacer
	from bokeh.plotting import figure, curdoc, show, output_file
	
	TOOLS = 'pan,wheel_zoom,box_select,lasso_select,reset'
	p = figure(tools=TOOLS, title='histoJesus')
	p.select(BoxSelectTool).select_every_mousemove = False
	p.select(LassoSelectTool).select_every_mousemove = False
	p.scatter(t, b, size=3, color='#3A5785', alpha=.6)
	output_file('wavform.html', title='scatter ex')
	hhist, hedges = np.histogram(a, bins=20)
	show(p)

def build_tf_model():
	t, a, b = [],[],[]
	for x in filepaths[:10]:	
		tabi = get_fft_from_filename_of_wave(x)
		print(len(tabi[0]),len(tabi[1]),len(tabi[2]))
		t.append(tabi[0]), a.append(tabi[1]), b.append(tabi[2])



# begin main and stuff

# fill variable filepaths with all the path addresses
filepaths = alternate_get_filename_and_location_index('EMOVO')

build_tf_model()

#graph_summed_fft()

#graph_wave()

#get_fft_from_filename_of_wave(filepaths[0])


