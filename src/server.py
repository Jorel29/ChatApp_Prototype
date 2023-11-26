import threading
import socket
import logging

logging.basicConfig(filename='server_log.log', level=logging.DEBUG)

#get hostname and ip and set ports
hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
sport = 8080
dport = 8082


#create and bind listening socket
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
