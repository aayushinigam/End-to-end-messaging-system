##COMMAND FOR SIGNUP - signup USERNAME PWD
## COMMAND FOR LOGIN - login USERNAME PWD

import socket
import sys
import threading

SEPERATOR = ";"
msg = ''


def signup(username,pwd) :
	global current_user
	name = input("Enter name :")
	roll_no = input("Enter roll no. :  ")
	msg = "signup;" + username + SEPERATOR + pwd +  SEPERATOR + name +  SEPERATOR + roll_no 
	current_user = username 
	client_sock.send(msg.encode())
	data = client_sock.recv(1024).decode()
	return data


def login(username,pwd) :
	global current_user
	msg = "login;" + username +  SEPERATOR + pwd 
	current_user = username
	client_sock.send(msg.encode())
	data = client_sock.recv(1024).decode()
	return data


def createGroup(group_name) :
	msg = "create;" + group_name 
	client_sock.send(msg.encode())
	data = client_sock.recv(1024).decode()
	return data

def joinGroup(group_name) :
	msg = "join;" + group_name + SEPERATOR + current_user
	client_sock.send(msg.encode())
	data = client_sock.recv(1024).decode()
	return data

def listGroups() :
	msg = "list;" 
	client_sock.send(msg.encode())
	data = client_sock.recv(1024).decode()
	return data

def sendMsgToPeer(username,msg) :
	msg = "send;" + username + SEPERATOR + msg + SEPERATOR + current_user
	client_sock.send(msg.encode())
	data = client_sock.recv(1024).decode()
	return data

def sendMsgToGroup(group_name,msg) :
	msg = "sendgroup;" + group_name + SEPERATOR + msg + SEPERATOR + current_user
	client_sock.send(msg.encode())
	data = client_sock.recv(1024).decode()
	return data


def receive():
    while True:
        try:
          data = client_sock.recv(1024).decode()
          username = ''
          if(";" in data) :
          	x = data.split(";")
          	username = (data.split(";"))[-1]
          	print(username + " : " + x[0])
          else :
          	print(data)
        except:
           pass

def write():
    while True :
    	inp = input()
    	parts = (inp.strip()).split(' ')
    	command = parts[0].lower()
    	if(command == 'signup') :
    		msg = signup(parts[1],parts[2])
    	elif(command == 'login') :
    		msg = login(parts[1],parts[2])
    	elif(command == 'join') :
    		msg = joinGroup(parts[1])
    	elif(command == 'create') :
    		msg = createGroup(parts[1])
    	elif(command == 'list') :
    		msg = listGroups()
    	elif(command == 'send') :
    		msg = sendMsgToPeer(parts[1],parts[2])
    	elif(command == 'sendgroup') :
    		msg = sendMsgToGroup(parts[1],parts[2])
    	print(msg)


groups = []
clients = []

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	client_sock.connect((socket.gethostname(), 12345))
except Exception as e :
	raise SystemExit(f"Connection failed : {e}")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()