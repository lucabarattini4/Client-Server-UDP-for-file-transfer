# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 16:11:35 2022

@author: Luca
"""

import socket as sk
import time
import pickle
import os
from os import listdir
from os.path import isfile, join

class Server:
  
  '''
  Initialize server
  '''
  def __init__(self):
    self.sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    self.server_address = ('localhost', 10000)
        
  '''
  Read all files in dir ./resources/ and put them in a list 
  '''
  def reload_file_list(self):
    try:
      self.file_list = [f for f in listdir("./resources/") if isfile(join("./resources/", f))]
      if not self.file_list:
        print("List Empty")
        return "EMPTY"
      else:
        return self.file_list
    except IOError:
      print("No files")
        
  '''
  Start server 
  '''
  def start_server(self):
    print ('\nStarting up on %s port %s' % self.server_address)
    self.sock.bind(self.server_address)
        
    while True:
      print('\nWaiting to receive message...')
      data, address = self.sock.recvfrom(4096)
      print('Received %s bytes from %s' % (len(data), address))
      print(data.decode('utf-8'))
      user_input = data.decode('utf-8')
      #Command "list"
      if user_input == "list":
        data1 = self.reload_file_list()
        message = pickle.dumps(data1)
        time.sleep(2)
        sent = self.sock.sendto(message, address)
        print ('Sent %s bytes back to %s' % (sent, address))
      #Command "get "
      elif user_input.startswith("get "):
        print("Get received")
        #-----------
        file_name = user_input.split('get ')[-1]
        #print(file_name)
        try:
          if file_name in self.reload_file_list():
            message = "OK"
            self.sock.sendto(message.encode(), address)
            file_size = os.path.getsize("./resources/" + file_name)
            print("File size: " + str(file_size) + " byte")
            print("Sending...")
                    
            self.sock.sendto(file_name.encode(), address)
            self.sock.sendto(str(file_size).encode(), address)
                    
            with open("./resources/" + file_name, "rb") as file:
              l = 0
              while l <= int(file_size):
                data = file.read(32768)
                if not (data):
                  break
                time.sleep(0.001)
                self.sock.sendto(data, address)
                l += len(data)
                print(str(l))  
            print("File transmitted")
            message = str(l)
            self.sock.sendto(message.encode(), address)
            file.close()
          else:
            print("File does not exist")
            message = "ERROR"
            self.sock.sendto(message.encode(), address)
        except Exception as info:
          print(info)
          message = "EXCEPTION"
          self.sock.sendto(message.encode(), address)
      #Command "put "
      elif user_input.startswith("put "):
        print('Put received')
        try:
          print('Waiting to receive...')
          #--------
          data, server = self.sock.recvfrom(4096)
          if(data.decode('utf-8') == "OK"):
            print("OK")
            file_name = self.sock.recv(100).decode('utf-8')
            file_size = self.sock.recv(100).decode('utf-8')
            #print("FILE NAME: " + file_name + " FILE SIZE: " + file_size + " byte")
                        
            with open("./resources/" + file_name , "wb") as file:
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
            if(data.decode('utf-8') == str(l)):
              print("Entire file received")
              message = "FileOK"
              self.sock.sendto(message.encode(), address)
            else:
              print("Part of file not arrived")
              message = "FileNotOK"
              self.sock.sendto(message.encode(), address)
            time.sleep(2)
            print ('Message received')
            file.close()
          else:
            print("File does not exist")
        except Exception as info:
          print(info)
      else:
        data1 = 'Command not found'
        time.sleep(2)
        sent = self.sock.sendto(data1.encode(), address)
        print ('Sent %s bytes back to %s' % (sent, address))
                
    def __str__(self):
      return "Server up on %s port %s" + str(self.server_address)
    
    
server = Server()
server.start_server()