from Tkinter import *
from tkFileDialog import askopenfilename
from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB
import time
import sys
import StringIO
import wave
import subprocess
import argparse
import sys
import subprocess
import re
import os
from os import listdir

HOME_FOLDER = '/home/miguel/Documents/GRABACIONES/'
EPS = 1e-1
CEIL = 5e-2

def main():
	parser = argparse.ArgumentParser(version='1.0',prog='Voice Recognition')
	parser.add_argument("-a", "--add", action="store_true", help="Add a new source")
	parser.add_argument("audio", type=str, help="Name of the audio file (*.wav)") 

	args = parser.parse_args()
	audio = HOME_FOLDER+args.audio
	db = GMMVoiceDB(HOME_FOLDER)	
	
	if args.add:
		print('Adding User...')
		name = str(time.strftime("%d%m%Y%H%M%S"))
		db.add_model(audio.split('.')[0], name)
		print('User '+name+' Added!')
	else:
		print('Recognition...')
		v = Voiceid(db, audio)
		v.diarization()	
		dic = db.get_speakers()
		dist = []
		d2u = {}
		for gender in dic:
			users = dic[gender]
			#print('Gender: ',gender)
			for u in users:
				#print(db.match_voice(audio, u, gender))
				dist.append(db.match_voice(audio, u, gender)[u])
				d2u[dist[-1]]=u
		
		dist.sort(None, None, True)
		if (dist[0]-dist[1]+CEIL)>EPS :
			print(d2u[dist[0]])
		else:
			print('unkonwn')
		
		print "Done!"

if __name__=='__main__':
	main()  
