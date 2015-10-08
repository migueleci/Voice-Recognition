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
			labels.append(name*10+counter)
			
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
	dis = {} 
	for i in range(100):
		ret, frame = video_capture.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				
		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.5,
			minNeighbors=5,
			minSize=(100, 100),
			flags=cv2.cv.CV_HAAR_SCALE_IMAGE
		)
		faces = fix_faces(faces)
		
		for (x, y, w, h) in faces:
			predict, conf = recognizer.predict(gray[y: y + h, x: x + w])
			if predict not in dis:
				dis[predict] = [-conf]
			elif len(dis[predict])<10:
				heapq.heappush(dis[predict], -conf)
			elif -conf > dis[predict][0]:
				heapq.heappop(dis[predict])
				heapq.heappush(dis[predict], -conf)
	
	best_dis = 100000
			
	for x in dis:	dis[x] = [-int(v) for v in dis[x]]
	for x in dis:	dis[x].sort()
	for x in dis:
		best_dis = min(best_dis, dis[x][-1])
		
	video_capture.release()
	cv2.destroyAllWindows()
	
	return best_dist
	
def main():
	images, labels = get_images_and_labels(pathDB)
	recognizer.train(images, np.array(labels))
	webcam()
	
main()
	
