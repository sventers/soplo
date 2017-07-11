

import glob
import tensorflow as tf
from tensorflow.contrib import ffmpeg

from scipy.io import wavfile
from scipy.fftpack import fft

from a_read_and_analysis import filepaths
print( '\nimports done now creating functions...\n')


def loadfiles(fname):
	binary = tf.read_file(fname)
	print ("binary is:     ", binary)
	return ffmpeg.decode_audio(binary, file_format='wav', samples_per_second=48000, channel_count=2)
#print ( loadfiles('EMOVO/f1/dis-f1-b1.wav') )

def preprocess(audio, rate=48000):
	# pad with 1 second of silence on either side
	front = tf.zeros([rate,2], dtype=audio.dtype)
	back = tf.zeros([rate - tf.mod(tf.shape(audio)[0], rate) + rate, 2], dtype=audio.dtype)
	audio = tf.concat([front, audio, back], 0)
	audio = tf.add(audio, tf.abs(tf.reduce_min(audio)))
	audio = tf.multiply(audio, 1.0/ tf.reduce_max(audio))
#	audio = tf.reshape(audio, [-1, int(rate * 
	return audio



# run init and do stuff

example_tf_wav = loadfiles(filepaths[0])
x = preprocess(example_tf_wav)
print (x)


tf.reset_default_graph()
with tf.Graph().as_default():
	files = glob.glob('EMOVO/*1/*.wav')
#	print (files)
	queue = tf.train.string_input_producer(files,num_epochs=1)
	fname = queue.dequeue()
	print (fname)
	audio = loadfiles(fname)
	audio = preprocess(audio)
	samples = tf.train.slice_input_producer([audio], num_epochs=1)
	batch = tf.train.batch(samples, 10)

	model = tf.identity(batch)

	init = [tf.global_variables_initializer(), tf.local_variables_initializer()]
	
	coord = tf.train.Coordinator()
	
	with tf.Session() as session:
		session.run(init)
		threads = tf.train.start_queue_runners(sess=session, coord=coord)
		for _ in range(10):
			try:
				result = session.run(model)
