'''
This is a naive dictionary attack script with a bit of multiprocessing for fun 
Linux only
'''

import time
import sys
import crypt
import multiprocessing as mp

def multi_run_wrapper(args):
   return deCript(*args)

def start_process():
    print 'Starting', mp.current_process().name

def  deCript(user, ctype, salt, Ppassword, rhash):
	if (ctype == '0'):
		insalt = salt
	else:
		insalt = '${}${}$'.format(ctype, salt)
	chash = crypt.crypt(Ppassword, insalt)
	if (rhash == chash):
		print user, Ppassword
	else:
		print "fail"
if __name__ == "__main__":
	passwordfile = open("password", 'r')
	userfile = open("shadow", 'r')
	passwords = []
	for line in passwordfile:
		if (line[0] == '#' or line[0] == '\n'):
			pass
		line = line.rstrip('\n')
		passwords.append(line)

	users = []
	ctypes = []
	salts = []
	rhashes = []

	for line in userfile:
		line = line.rstrip('\n')
		line = line.split(":")
		hashpass = line[1].split('$')
		users.append(line[0])
		rhashes.append(line[1])
		if (len(hashpass) > 1):
			ctypes.append(hashpass[1])
			salts.append(hashpass[2])
		else:
			ctypes.append('0')
			salts.append(line[1][0:2])

	tasks = []
	for i in range(len(users)):
		for j in range(len(passwords)):
			tasks.append((users[i], ctypes[i], salts[i], passwords[j], rhashes[i]))
	
	pool_size = mp.cpu_count()*2

	pool = mp.Pool(processes=pool_size)
	time.sleep(1)
	pool.map(multi_run_wrapper,tasks)


