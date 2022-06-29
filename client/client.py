# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 16:11:33 2022

@author: Luca
"""

import socket as sk
import time
import pickle
import os
from os import path

class Client:
  
  '''
  Initialize client
  '''
  def __init__(self):
    self.sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    self.server_address = ('localhost', 10000)

  '''
  Ask server for the list of available files
  '''
  def list_file(self):
    try:
      self.sock.connect(self.server_address)
      #send message
      message = "list"
      print("Sending request...")
      time.sleep(0.1)
      self.sock.sendto(message.encode(), self.server_address)

      print("Waiting to receive...")
      data, server = self.sock.recvfrom(4096)
      f_list = pickle.loads(data)
      if f_list != "EMPTY":
        print("\nFILE LIST (insert file name without number)")
        i = 1
        for f in f_list:
          print(str(i) + "- " + str(f))
          i += 1
      else:
        print("Server has no files")
    except Exception as info:
      print(info)

  '''
  Download file from server 
  '''
  def get_file(self, name):
    try:
      self.sock.connect(self.server_address)
      message = "get " + name
      print("Sending request...")
      time.sleep(2)
      self.sock.sendto(message.encode(), self.server_address)

      print("Waiting to receive...")
      data, server = self.sock.recvfrom(4096)
      if(data.decode('utf-8') == "OK"):
        file_name = self.sock.recv(100).decode()
        file_size = self.sock.recv(100).decode()
        #print("FILE NAME: " + str(file_name) + " SIZE: " + str(file_size))

        with open("./received/" + file_name, "wb") as file:
          l = 0
          while l < int(file_size):
            data = self.sock.recv(32768)
            if not (data):
              break
            file.write(data)
            l += len(data)
            #print(str(l) + " data: " + str(data))  
        print("File transfer completed")
        file.close()

        data, server = self.sock.recvfrom(4096)
        if data.decode('utf-8') == str(l):
          print("Entire file received")
        else:
          print("Part of file not received")

        time.sleep(2)
        print("Message received")
        file.close()
      else:
        print("File does not exist")
    except Exception as info:
      print(info)

  '''
  Upload file from client to server
  '''
  def put_file(self, file_name):
    try:
      self.sock.connect(self.server_address)
      message = 'put ' + file_name
      print ('Sending request...')
      time.sleep(2) 
      self.sock.sendto(message.encode(), self.server_address)
            
      if path.isfile("./myFiles/" + file_name):
        print("IL FILE ESISTE")
        message = "OK"
        self.sock.sendto(message.encode(), self.server_address)
        file_size = os.path.getsize("./myFiles/" + file_name)
        #print("FILE SIZE: " + str(file_size) + " byte")
        self.sock.sendto(file_name.encode(), self.server_address)
        self.sock.sendto(str(file_size).encode(), self.server_address)
                
        with open("./myFiles/" + file_name, "rb") as file:
          l = 0          
          while l <= int(file_size):
            data = file.read(32768)
            if not (data):
              break
            time.sleep(0.001)
            self.sock.sendto(data, self.server_address)
            l += len(data)
            #print(str(l))        
        #print("File transmitted")
        message = str(l)
        self.sock.sendto(message.encode(), self.server_address)      
        file.close()
        data, server = self.sock.recvfrom(4096)
        if data.decode('utf-8') == "FileOK":
          print("File ok")
        else: 
          print("File not ok")
      else:
        print("File does not exixst")
        message = "ERROR"
        self.sock.sendto(message.encode(), self.server_address)
    except Exception as info:
      print(info)

  '''
  Close socket
  '''
  def close_connection(self):
    self.sock.close()

  '''
  Print client
  '''
  def __str__(self):
    return "I'm the client"


client = Client()
check = True

while check:
  value = input("What do you want to do?\n")
  if value.lower() == "list":     
    print("\nGetting file list from server...")
    client.list_file()  
  elif value.lower().startswith("get ") and value.split('get ')[-1] != "":
    print("\nDownloading " + value.split('get ')[-1] + " from server...")
    client.get_file(value.split('get ')[-1])      
  elif value.lower().startswith("put ") and value.split('put ')[-1] != "":     
    print("\nUploading " + value.split('put ')[-1] + " to server...")
    client.put_file(value.split('put ')[-1])
  elif value.lower() == "close":
    print("\nClosing connection...")
    client.close_connection()
    check = False
  else:
    print("ERROR: incorrect command or syntax")