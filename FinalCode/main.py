
FILE = 'UserList.txt'
user_list = []

def read_user_list():
	global user_list
	f = open(FILE, 'r')
	for line in f:
		line=line[0:-1]
		if len(line) > 0: user_list.append(int(line))
	
def write_user_list():
	f = open(FILE, 'w')
	for user in user_list:
		f.write(str(user)+'\n')

#name -> Path of the user's name file (.wav)
#voice -> Path of the user's voice file (.wav)
#photo -> Path of the user's photo file (.jpg)
def add_user(name, voice, photo):
	global user_list
	user_name = user_list[-1] + 1 if len(user_list) > 0 else 1;
	user_list.append(user_name)
	#add voice (wav file) to DataBase - Voice Recognition Script
	#add photo (jpg or jpeg file) to DataBase - Copy file into Face path

#name -> Path of the user file to be removed (.wav)
def remove_user(name):
	user_name = int((name.split('.')[0]).split('/')[-1])
	user_list.remove(user_name)
	#remove voice (wav file) from DataBase
	#remove photo (jpg or jpeg file) from DataBase

def recognize_user(voice):
	#v_prec = Voice Recognition Script
	#f_prec = Face Recognition Script
	return True if v_prec != 'unknown' and f_prec < 100 else False
	
def main():
	read_user_list()
	#parser to add, remove or recognize an User.
	write_user_list()

main()
