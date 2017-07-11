
import glob
import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib.pyplot import specgram
from a_read_and_analysis import filepaths

from scipy.integrate import odeint
from bokeh.plotting import figure, show, output_file
print ('\nloading successful...\n')


def load_sound_bits(file_paths):
	raw_sounds = []
	for fp in file_paths:
		X, sr = librosa.load(fp)
		raw_sounds.append(X)
		print (X)
	return raw_sounds

def plot_waves(sound_names, raw_sounds):
	i=1
	fig = plt.figure(figsize=(25,60), dpi = 900)
	for n,f in zip(sound_names, raw_sounds):
		plt.subplot(10,1,i)
		librosa.display.waveplot(np.array(f),sr-22050)
		plt.title(n.title())
		i += 1
	plt.suptitle('Figure 1: Waveplot', x=.5, y=.915, fontsize=18)
	plt.show()

def plot_specgram(sound_names, raw_sounds):
	i = 1
	fig = plt.figure(figsize(25,60), dpi = 900)
	for n, f in zip(sound_names, raw_sounds):
		plt.subplot(10,1,i)
		specgram(np.array(f), Fs=22050)
		plt.title(n.title())
		i += 1
	plt.suptitle('Figure 2: spectogram', x=.5, y=.915, fontsize=18)
	plt.show()

def plot_bokeh():

	pass

# run loops
file_links_1_third = glob.glob('EMOVO/*1/*.wav')


raw_sounds = load_sound_bits(file_links_1_third[:5])

print (raw_sounds[0])

#plot_waves(x[:5], raw_sounds)
#plot_specgram(x[:5], raw_sounds)



