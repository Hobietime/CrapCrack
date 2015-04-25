import multiprocessing as mp
import time
from itertools import permutations
def multi_run_wrapper(args):
   return add(*args)

def add(user, ctype, salt, Ppassword, rhash):
    print user, ctype, salt, Ppassword, rhash

def start_process():
    print 'Starting', mp.current_process().name

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
		for j in [''.join(p) for p in permutations('abcdefghijklmnopqrstuvwxyz', 6)]:
			tasks.append((users[i], ctypes[i], salts[i], j, rhashes[i]))
	
	pool_size = mp.cpu_count()*2

	pool = mp.Pool(processes=pool_size, initializer=start_process, maxtasksperchild=2, )
	time.sleep(1)
	results = pool.map(multi_run_wrapper,tasks)