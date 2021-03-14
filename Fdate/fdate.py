# When making the index of the disk run this file in command  prompt, it will not work in linux.
import os
import re
import time 
import argparse
import pickle
from threading import Thread

t1 = time.time()
dict1 ={}
i = 1
def get_drives():  # get all the drives
	resp =os.popen('wmic logicaldisk get caption')
	drive = resp.read()
	return drive.split()[1:]
	
def creating_index(path):  # to create index at particular path 
	global i
	resp =os.walk(path)
	for root,d,files  in resp:
		for file in files:
			path1 = root+"\\"+file 
			cr_time = os.path.getctime(path1)
			md_time = os.path.getmtime(path1)
			dict1[path1] = (cr_time, md_time)
	#print (dict1)


def create_index():	 # get all the drives and one to all creating_index
	list1_th = []
	#for d in get_drives():
	for d in ['G:']:
		print (d)
		th1 = Thread(target=creating_index, args=(d+"\\",))
		list1_th.append(th1)
		th1.start()

	for th1 in list1_th:
		th1.join()
	fw = open("fdate.index","wb")
	pickle.dump(dict1,fw)
	fw.close()
	t2 = time.time()
	print ("Index created, time taken", t2-t1)
# fdate -cs 100

def h_e(hr):

	# human_time --> 9tuple format --> epoch 

	t9=time.strptime(hr,"%Y-%m-%d %H:%M:%S")
	print (t9)

print (time.mktime(t9)) # local time

def search(t_gap, t_given=0, c_or_m='C', match1=None):  # To search a file 
	t3 = time.time()
	fr = open("fdate.index","rb")
	data1 = pickle.load(fr)
	fr.close()
	print ("Here*******")
	
		
	t_given = int(time.time()) - t_given

	t_gap = int(t_gap)
	t_old = int(time.time()) -t_gap    # 100 t_old sec ago to now how many files
	print ("-l", time.ctime(t_given))
	print ("old c", time.ctime(t_old))
	if t_gap < t_given:
		for k,v in data1.items():# k file_path v (c,m)
			#print (k,v)
			ctime, mtime = v 
			f_time = ctime 
			#print ("Here2")
			#import pdb; pdb.set_trace()

			if f_time > t_old and f_time < t_given:
				#print ("Here3")
				if match1 :
					m = re.search(match1, k)
					if m :
						print (time.ctime(f_time),":", k )
				else :
					print (time.ctime(f_time),":", k )
					
	else :
		print ("Please give the right range ")


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("file_name", nargs="?")
	parser.add_argument("-c", help="Create index", action='store_true')
	parser.add_argument('-cs', nargs='?', help='seconds Main option', type=int)
	parser.add_argument('-l', nargs="?", help='range ', default=0)
	parser.add_argument('-et', nargs="?", help="2015-10-20 16:09:22")
	
	args = parser.parse_args()
	print (args)
	try:
		if args.c:
			create_index()
			
		else:
			if args.cs:
				t_gap = args.cs
				t_given= args.l
				if isinstance(args.cs, int):
					t_given = int(args.l)

				search(t_gap, t_given, c_or_m='C', match1=None)
				
			if args.et:
				
				t_gap = h_e(args.et)
				t_given= h_e(args.l)
				if isinstance(args.cs, int):
					t_given = int(args.l)

				search(t_gap, t_given, c_or_m='C', match1=None)
				
			

				
				
			
	except Exception as e :
		print (e)
			
main()
