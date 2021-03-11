# run this file in command  prompt, it will not work in linux.

import re
import os
import time
import argparse
from threading import Thread
import pickle

dict1={}
i=1
t1=time.time()
def get_drives():#getting all drives
    resp=os.popen('wmic logicaldisk get caption')#wmic logicaldisk get caption which gets all the drives present on the computer and stores it in a file resp.
    drive=resp.read()
    return drive.split()[1:]

def creating_index(path):#creating index of particluar path
    global i
    resp=os.walk(path)
    for root,d,files in resp:
        for file in files:
            path1=root+"\\"+file
            file1=file
            if file1 in dict1:
                file1=file1+'|'+str(i)
                i=i+1
            dict1[file1]=path1

def Create_index():#creating index of total disk
    list1_th=[]
    for d in get_drives():
         print(d)
        creating_index(d+"\\")
        th1=Thread(target=creating_index, args=(d+"\\",))
        list1_th.append(th1)
        th1.start()

    for th1 in list1_th:
        th1.join()

    fw=open("finder.index","wb")
    pickle.dump(dict1,fw)
    fw.close()
    t2 = time.time()
    print("Index Created, time taken ", t2-t1)
            
def search(file1):
    t3 = time.time()               #to search a file
    fr=open("finder.index", "rb")
    data1=pickle.load(fr)
    fr.close()
    for k,v in dict1.items():
        k=k.split("|")[0]
        m=re.search(file1,k,re.I)
        if m:

            print(k, ":", v)
    t4 = time.time()
    print("time to search", t4-t3)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("file_name", nargs='?')
    parser.add_argument("-c", help="Create Index", action='store_true')
    args=parser.parse_args()
    print(args)
    try:
        if args.c:
            Create_index()
        else:
            if args.file_name=="" or args.file_name==None:
                print("Please give the file name")
            else:

                search(args.file_name)
    except Exception as e:
        print(e)

main()

# path = "C:\\Users\\praveen\\Downloads\\Cert"
# for d in get_drives():
#   print(d)
#   creating_index(d+"\\")
# t2 = time.time()
# print("Index Created, time taken ", t2-t1)
# file1 = input("Enter the file to be searched ")
# search(file1)