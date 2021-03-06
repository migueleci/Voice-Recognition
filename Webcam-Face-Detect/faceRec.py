import cv2
import sys
import os
import numpy as np
from PIL import Image
import heapq

pathDB = 'DB'
cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
recognizer =  cv2.createLBPHFaceRecognizer()

def get_images_and_labels(path):
	image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
	images = []
	labels = []
	count = 2000
	for image_path in image_paths:
		counter = 0
		image_pil = Image.open(image_path).convert('L')
		image2 = cv2.imread(image_path)
		image = np.array(image_pil, 'uint8')
		gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
		name=int(os.path.split(image_path)[1].split(".")[0])
		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.5,
			minNeighbors=5,
			minSize=(100, 100),
			flags = cv2.cv.CV_HAAR_SCALE_IMAGE
		)
		for (x, y, w, h) in faces:
			images.append(image[y: y + h, x: x + w])
			counter +=1
			#count += 1
			labels.append(name*10+counter)
			cv2.cv.SaveImage('{0}.jpg'.format(name*10+counter), cv2.cv.fromarray(image[y: y + h, x: x + w]))
			#print (str(name*10+counter))
			#cv2.waitKey(150)
	return images, labels

def fix_faces(faces):
	faces = [tuple(f) for f in faces]
	def face_in_face(f0,f1):
		(x0,y0,w0,h0) = f0
		(x1,y1,w1,h1) = f1
		if x0>x1+w1 or x1>x0+w0 or y0>y1+h1 or y1>y0+h0:
			return False
		xi = max(x0,x1)
		wi = min(x0+w0,x1+w1)-xi
		yi = max(y0,y1)
		hi = min(y0+h0,y1+h1)-yi
		A0 = w0*h0
		Ai = wi*hi
		return Ai >= .75 * A0
	s = set(faces)
	for f0 in faces:
		for f1 in faces:
			if f1!=f0 and f1 in s and face_in_face(f0,f1):
				s.discard(f1)
	return list(s)

def webcam():
	found = False
	min_predict = 100000
	dis = {} 
	for i in range(100):
		# Capture frame-by-frame
		ret, frame = video_capture.read()
		#cv2.cv.SaveImage('{0}.jpg'.format(counter2), cv2.cv.fromarray(frame))
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				
		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.5,
			minNeighbors=5,
			minSize=(100, 100),
			flags=cv2.cv.CV_HAAR_SCALE_IMAGE
		)
		faces = fix_faces(faces)
			
		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			color = (0, 255, 0) if len(faces)==1 else (255, 0, 0)
			nbr_predicted, conf = recognizer.predict(gray[y: y + h, x: x + w])
			#cv2.cv.SaveImage('{0}.jpg'.format(counter), cv2.cv.fromarray(gray[y: y + h, x: x + w]))
			#counter += 1
			isbetter = True
			if nbr_predicted not in dis:
				dis[nbr_predicted] = [-conf]
			elif len(dis[nbr_predicted])<10:
				heapq.heappush(dis[nbr_predicted], -conf)
			elif -conf > dis[nbr_predicted][0]:
				heapq.heappop(dis[nbr_predicted])
				heapq.heappush(dis[nbr_predicted], -conf)
			else:
				isbetter = False
			
			if isbetter:
				cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
			
		# Display the resulting frame
		#cv2.imshow('Video', frame)
		#if cv2.waitKey(1) & 0xFF == ord('q'): break
		#for x in dis:
		#	if len(dis[x])==10 and dis[x][0]>-100 : found = True
	
	for x in dis:	dis[x] = [-int(v) for v in dis[x]]
	for x in dis:	dis[x].sort()
	for x in dis:
		print 'Person %d : %d ... %d' % (x, dis[x][0], dis[x][-1])
		
	# When everything is done, release the capture
	video_capture.release()
	cv2.destroyAllWindows()

def main():
	images, labels = get_images_and_labels(pathDB)
	recognizer.train(images, np.array(labels))
	webcam()
	
main()
	
