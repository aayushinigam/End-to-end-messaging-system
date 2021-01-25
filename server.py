import socket
import threading
import os
import sys
 

groups = []
clients = []
sockets_list = []


class Group :
	def __init__(self,group_name,participants,group_secret) :
		self.group_name = group_name
		self.participants = []
		self.group_secret = group_secret

	def addParticipants(participant) :
		participants.append(participant)


class Clients :
	def __init__(self,name,roll_no,username,password,client_sock) :
		self.name = name
		self.roll_no = roll_no
		self.username = username
		self.password = password
		self.client_sock = client_sock

def getSocket(username) :
	for x in sockets_list :
		for key in x :
			if(key == username) :
				return x[key]


def signup(info, client_sock) :
	global new_client
	username = info[1]
	#print(username)
	msg = ''
	#Check if user already exists :
	if(not any(x.username == username for x in clients)) :
		password = info[2]
		name = info[3]
		roll_no = info[4]
		new_client = Clients(name,roll_no,username,password,client_sock)
		clients.append(new_client)
		temp = {username : client_sock}
		sockets_list.append(temp)
		msg = "Signed up successfully!"
	else :
		msg = "User already exists"
	print(msg)
	return msg


def login(info,client_sock) :
	username = info[1]
	pwd = info[2]
	if(username in sockets_list) :
		msg = "user already logged in"
		return msg
	temp = {username : client_sock}
	sockets_list.append(temp)
	if(any(x.username == username for x in clients)) :
		flag = False
		for x in clients :
			if(x.username == username and x.password == pwd) :
				msg = "logged in successfully"
				flag = True
		if(not flag) :
			msg = "Wrong credentials"

	else :
		msg = "User doesn't exist"
	print(msg)
	return msg


#create new group
def createGroup(info,flag) :
	if(flag) :
		group_name = info[1]
		participants = []
		group_secret = 0
	else :
		group_name = info
		group_secret = 0
	msg = ''
	if(any(x.group_name == group_name for x in groups)) :
		msg = "Group already exists"
	else :
		new_group = Group(group_name,participants,group_secret)
		groups.append(new_group)
		msg = "Group created successfully"
	print(msg)
	return msg


#Join a group
def joinGroup(info) :
	group_name = info[1]
	print("group name is : " + group_name)
	member = info[2]
	print("member is :" + member)
	flag = False
	msg = ''
	group_secret = 0
	#group doesn't exist --- create a new group
	for x in groups :
		if(x.group_name == group_name) :
			print("group exists")
			x.participants.append(member)
			flag = True
			break
	if(not flag) :
		print("group doesn't exist")
		participants = [member]
		new_group = Group(group_name,participants,group_secret)
		groups.append(new_group)

	msg = "group joined successfully"
	return msg


#List all the available groups
def listGroups() :
	print("inside list groups ")
	msg = ''
	if(len(groups) > 0) :
		for x in groups :
			msg += x.group_name
			msg += ';'
	else :
		msg = "No group found!"
	print(msg)
	return msg

def sendMsgToPeer(info) :
	receiver  = info[1]
	msgToSend = info[2]
	sender = info[3]
	flag = False
	client_sock = ''
	for i in sockets_list :
		for key in i :
			if(key == receiver) :
				flag = True
				client_sock = i[key]
				break
	if(flag) :
		msgToSend +=  ";" + sender
		client_sock.send(bytes(msgToSend,"utf-8"))
		msg = "message sent successfully"
	else :
		msg = "username doesn't exist"
	print(msg)
	return msg


def sendMsgToGroup(info) :
	group_name = info[1]
	msgToSend = info[2]
	sender = info[3] 
	flag = False  #to check if group exists
	senderIsMember = False  #to check if sender is the member of the group
	msg = ''
	print(type(msgToSend))
	msgToSend += ";" + sender
	for x in groups :
		if(x.group_name == group_name) :
			flag = True
			for username in x.participants :
				if(username == sender) :
					senderIsMember = True
					continue
				client_sock = getSocket(username)
				client_sock.send(bytes(msgToSend,"utf-8"))
	if(not flag) :
		msg = "group doesn't exist"
	if(not senderIsMember) :
		msg = "sender is not the member of the group"
	msg = "message sent successfully"
	print(msg)

	return msg
	






#create new client
def newClient(client_sock,addr) :
	while True:
		msg = ''
		data = client_sock.recv(1024).decode()
		info = data.split(";")
		command = info[0].lower()
		if(command == 'signup') :
			msg = signup(info,client_sock)
		elif(command == 'login') :
			msg = login(info,client_sock)
		elif(command == 'join') :
			msg = joinGroup(info)
		elif(command == 'create') :
			msg = createGroup(info,True)
		elif(command == 'list') :
			msg = listGroups()
		elif(command == 'send') :
			msg = sendMsgToPeer(info)
		else :
			msg = sendMsgToGroup(info)
		client_sock.send(bytes(msg,"utf-8"))

	client_sock.close()





#main() CODE 
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((socket.gethostname(), 12345))
server_sock.listen()
while True :
	try :
		client, addr = server_sock.accept()
		#new thread for every client
		threading._start_new_thread(newClient,(client,addr))
	except KeyboardInterrupt as e :
		printf("server shutting down")

server_sock.close()








