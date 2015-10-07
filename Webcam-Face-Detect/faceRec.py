import cv2
import sys
import os
import numpy as np
from PIL import Image

pathDB = '/home/lenovo/Documentos/Webcam-Face-Detect/DB/'
cascPath = '/home/lenovo/Documentos/Webcam-Face-Detect/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
recognizer =  cv2.createLBPHFaceRecognizer()

def get_images_and_labels(path):
	image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
	images = []
	labels = []
	#count = 2000
	for image_path in image_paths:
		counter = 0
		image_pil = Image.open(image_path).convert('L')
		image2 = cv2.imread(image_path)
		image = np.array(image_pil, 'uint8')
		gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
		name=int(os.path.split(image_path)[1].split(".")[0])
		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.2,
			minNeighbors=5,
			minSize=(60, 60),
			flags = cv2.cv.CV_HAAR_SCALE_IMAGE
		)
		for (x, y, w, h) in faces:
			images.append(image[y: y + h, x: x + w])
			counter +=1
			#count += 1
			labels.append(name*10+counter)
			#cv2.cv.SaveImage('{0}.jpg'.format(count), cv2.cv.fromarray(image[y: y + h, x: x + w]))
			#print (str(name*10+counter))
			#cv2.waitKey(150)
	return images, labels

def webcam():
	found = False
	#counter = 100
	#counter2 = 9900
	while not found:
		# Capture frame-by-frame
		ret, frame = video_capture.read()
		#cv2.cv.SaveImage('{0}.jpg'.format(counter2), cv2.cv.fromarray(frame))
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				
		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.2,
			minNeighbors=5,
			minSize=(60, 60),
			flags=cv2.cv.CV_HAAR_SCALE_IMAGE
		)

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			nbr_predicted, conf = recognizer.predict(gray[y: y + h, x: x + w])
			#cv2.cv.SaveImage('{0}.jpg'.format(counter), cv2.cv.fromarray(gray[y: y + h, x: x + w]))
			#counter += 1
			#print nbr_predicted, conf
			if conf < 20:
				found = True
				cv2.imshow('Identified', gray[y: y + h, x: x + w])
				print('User recognized '+str(nbr_predicted))
				cv2.waitKey(1000)
			
		# Display the resulting frame
		cv2.imshow('Video', frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything is done, release the capture
	video_capture.release()
	cv2.destroyAllWindows()

def main():
	images, labels = get_images_and_labels(pathDB)
	cv2.destroyAllWindows()
	recognizer.train(images, np.array(labels))
	webcam()
	
main()
	
