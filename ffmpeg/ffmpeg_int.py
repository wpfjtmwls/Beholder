import subprocess as sp
import numpy
from os.path import join, dirname
import logging

FFMPEG_BIN = "ffmpeg"
#with open(img_path, 'rb') as FFMPEG_IMG

def grab_frame(in_path, out_path):
	# command line ffmpeg -i inputfile -ss time -vframes #offrames out.png outputname
	command = [ FFMPEG_BIN,
		    '-i', in_path,
		    '-ss', '00:00:00.01',
		    '-vframes', '1',
		    out_path]
	# getting the output image from CLI
	pipe = sp.call(command, stdout = sp.PIPE)
	## read 420*360*3 bytes (= 1 frame)
	#raw_image = pipe.stdout.read(420*360*3)
	## transform the byte read into a numpy array
	#image =  numpy.fromstring(raw_image, dtype='uint8')
	#image = image.reshape((360,420,3))
	## throw away the data in the pipe's buffer.
	#pipe.stdout.flush()
	
