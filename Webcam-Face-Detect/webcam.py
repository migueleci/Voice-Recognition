import cv2
import sys
import os
import numpy as np
from PIL import Image

#cascPath = sys.argv[1]
cascPath = '/home/lenovo/Documentos/Webcam-Face-Detect/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
recognizer =  cv2.createLBPHFaceRecognizer()
recognizer1 =  cv2.createEigenFaceRecognizer()
#recognizer2 =  cv2.createFisherFaceRecognizer()

def get_images_and_labels2(path):
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
			scaleFactor=1.2,
			minNeighbors=5,
			minSize=(60, 60),
			flags = cv2.cv.CV_HAAR_SCALE_IMAGE
		)
		for (x, y, w, h) in faces:
			images.append(image[y: y + h, x: x + w])
			counter +=1
			count += 1
			labels.append(name*10+counter)
			cv2.cv.SaveImage('{0}.jpg'.format(count), cv2.cv.fromarray(image[y: y + h, x: x + w]))
			print (str(name*10+counter))
			cv2.waitKey(150)
	return images, labels
	
def get_images_and_labels(path): 
	# Append all the absolute image paths in a list image_paths
	# We will not read the image with the .sad extension in the training set
	# Rather, we will use them to test our accuracy of the training
	image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
	# images will contains face images
	images = []
	# labels will contains the label that is assigned to the image
	labels = []
	for image_path in image_paths:
		counter = 0
		# Read the image and convert to grayscale
		image_pil = Image.open(image_path).convert('L')
		# Convert the image format into numpy array
		image = np.array(image_pil, 'uint8')
		# Get the label of the image
		nbr = int(os.path.split(image_path)[1].split(".")[0])
		# Detect the face in the image
		faces = faceCascade.detectMultiScale(image)
		# If face is detected, append the face to images and the label to labels
		for (x, y, w, h) in faces:
			images.append(image[y: y + h, x: x + w])
			counter+=1
			labels.append(nbr*10+counter)
			cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
			cv2.waitKey(50)
			# return the images list and labels list
	return images, labels

def recognize(path):
	image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
	for image_path in image_paths:
		predict_image_pil = Image.open(image_path).convert('L')
		predict_image = np.array(predict_image_pil, 'uint8')
		faces = faceCascade.detectMultiScale(predict_image)
		for (x, y, w, h) in faces:
			nbr_actual = os.path.split(image_path)[1].split(".")[0]
			nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
			print nbr_predicted, conf, nbr_actual
			#nbr_predicted, conf = recognizer1.predict(predict_image[y: y + h, x: x + w])
			#print nbr_predicted, conf, nbr_actual
			#nbr_predicted, conf = recognizer2.predict(predict_image[y: y + h, x: x + w])
			#print nbr_predicted, conf, nbr_actual
			'''
			if nbr_actual == nbr_predicted:
				print "{} is Correctly Recognized with confidence {}".format(nbr_actual, conf)
			else:
				print "{} is Incorrectly Recognized as {}".format(nbr_actual, nbr_predicted)'''
			cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
			cv2.waitKey(1000)
			

def webcam():
	found = False
	counter = 100
	counter2 = 9900
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
			cv2.cv.SaveImage('{0}.jpg'.format(counter), cv2.cv.fromarray(gray[y: y + h, x: x + w]))
			counter += 1
			print nbr_predicted, conf
			if conf < 35:
				found = True
				cv2.imshow('Identified', gray[y: y + h, x: x + w])
			
		# Display the resulting frame
		cv2.imshow('Video', frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything is done, release the capture
	video_capture.release()
	cv2.destroyAllWindows()


def database():
	pathDB = '/home/lenovo/Documentos/Webcam-Face-Detect/DB/'
	pathP = '/home/lenovo/Documentos/Webcam-Face-Detect/Photos/'
	# The folder yalefaces is in the same folder as this python script
	# Call the get_images_and_labels function and get the face images and the
	# corresponding labels
	#images, labels = get_images_and_labels(pathDB)
	images, labels = get_images_and_labels2(pathDB)
	cv2.destroyAllWindows()
	recognizer.train(images, np.array(labels))
	#recognizer1.train(images, np.array(labels))
	#recognizer2.train(images, np.array(labels))
	#recognize(pathP)
	webcam()
	
database()
	
