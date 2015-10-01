from Tkinter import *
from tkFileDialog import askopenfilename
from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB
import time
import sys
import StringIO
import pyaudio
import wave
import subprocess

HOME_FOLDER = '/home/miguel/Documents/GRABACIONES/'
EPS = 1e-1
CEIL = 5e-2

def recordAudio():
	global audio, labelA

	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = 5
	#audio = "recording"
	audio = str(time.strftime("%d%m%Y%H%M%S"))
	labelA["text"] = "File: "+audio+".wav"
	WAVE_OUTPUT_FILENAME = audio+".wav"

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)

	print("* recording")
		
	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	print("* done recording")

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

def selectFile():
	global audio, tk, labelA
	file_opt = options = {}
	options['defaultextension'] = '.wav'
	options['filetypes'] = [('audio files', '.wav')]
	options['title'] = 'Select audio file'
	audioName = askopenfilename(**file_opt)
	if audioName != None:
		name = audioName.split("/")[-1]
		audio = audioName.split(".")[0]
		labelA["text"] = "File: "+name

def addUser():
	global audio, db
	if audio != None:
		name = str(time.strftime("%d%m%Y%H%M%S"))
		db.add_model(audio, name)
		print 'User '+name+' Added'
	else :
		print 'Record audio first!'

def recognition():
	global audio, db, label
	if audio != None:
		print 'Comparing...'
		#dic = db.get_speakers()
		v = Voiceid(db, audio+'.wav')
		#v.extract_speakers()
		v.diarization()	
		dic = db.get_speakers()
		dist = []
		d2u = {}
		for gender in dic:
			users = dic[gender]
			print('Gender: ',gender)
			for u in users:
				print(db.match_voice(audio+'.wav', u, gender))
				dist.append(db.match_voice(audio+'.wav', u, gender)[u])
				d2u[dist[-1]]=u
		
		print('--------------')
		print("Best Speaker (Own)")		
		dist.sort(None, None, True)
		print( (dist[0]-dist[1]+CEIL),EPS,dist )
		if (dist[0]-dist[1]+CEIL)>EPS :
			print(d2u[dist[0]])
		
		#print(dic)
		print('--------------')
		print("Best Speaker")
		print("Audio: ",audio.split('/')[-1])
		v.extract_speakers(False, True)
		for c in v.get_clusters():
			cluster = v.get_cluster(c)
			print(cluster.get_best_speaker() )
			print('------------')
		
		'''
		print 'Comparing...'
		v = Voiceid(db, audio+'.wav')
		#s = StringIO.StringIO()
		#with s as sys.stdout:
		v.extract_speakers(False, True)
		#with open('output.txt','w') as sys.stdout:
		for c in v.get_clusters():
			cluster = v.get_cluster(c)
			user = cluster.get_best_speaker() 
			print('------------')
			if user != "unknown":
				print("Best Speaker: %s" % (user) )
				print("Speaker: %s" % (cluster.get_speaker()) )
				print("Gender: %s" % (cluster.get_gender()) )
				print("Distance: %s" % (cluster.get_distance()) )
				print("Mean: %s" % (cluster.get_mean()) )
				print("Dist. from mean: %s" % (cluster.get_m_distance()) )
				print("Best five speakers: " % (cluster.get_best_five()) )
			else:
				print("User Unknown")
				print("Gender: %s" % (cluster.get_gender()) )
				print("Distance: %s" % (cluster.get_distance()) )
				print("Best five speakers: " % (cluster.get_best_five()) )
			print('------------')
		#sys.stdout = sys.__stdout__
		
		#labelB["text"] = "Users: " + str(listName)'''
		print "Done!"
	else :
		print 'Record audio first!'

def cleanDataBase():
	global db
	subprocess.check_output("rm -rf "+HOME_FOLDER+"M/",shell=True)
	subprocess.check_output("rm -rf "+HOME_FOLDER+"U/",shell=True)
	subprocess.check_output("rm -rf "+HOME_FOLDER+"F/",shell=True)
	db = GMMVoiceDB(HOME_FOLDER)
	print("Data Base cleaned!")

def test2():
	global frame, label, tk, labelA
	frame = Frame(tk)
	frame.pack(fill=X)
	#canvas = Canvas(frame, bg="grey", width=600, height=600)
	#canvas.pack()
	label = Label(frame, width=30, height=1)
	label.pack()
	audioR = Button(frame, text="Record Audio", command=recordAudio)
	audioR.pack()
	audioS = Button(frame, text="Select Audio", command=selectFile)
	audioS.pack()
	labelA = Label(frame, text="File: None", width=30, height=3)
	labelA.pack()
	add_user = Button(frame, text="Add User", command=addUser)
	add_user.pack()
	recog = Button(frame, text="Recognition", command=recognition)
	recog.pack()
	labelB = Label(frame, text="Users: Unknown", width=30, height=3)
	labelB.pack()
	cleanDB = Button(frame, text="Clean DB", command=cleanDataBase)
	cleanDB.pack()
	labelC = Label(frame, width=30, height=1)
	labelC.pack()
            
def main():
	global db, tk, audio
	audio = None
	db = GMMVoiceDB(HOME_FOLDER)	
	tk = Tk()
	tk.title("Speech Recognition")
	tk.maxsize(1000, 400)
	test2()
	tk.mainloop()
	
if __name__ == '__main__':
	main()
