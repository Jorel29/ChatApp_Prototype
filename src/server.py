import threading
import socket
import logging

logging.basicConfig(filename='server_log.log', level=logging.DEBUG)

# get hostname and ip and set ports
hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
sport = 8080
dport = 8082

clients = []

# create and bind listening socket for clients to send to
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind((hostip, sport))

logging.info(f'I\'m a signaling server')

# listen for client connections
# note: input is not fully sanitized
# waits for <clientip>:<serverip> message format
def listen():
    while True:
        try:
            data = sock.recv(1024).decode(encoding='utf-8', errors='strict')
        except:
            logging.warning(f'Decode error from incoming message from a client')
            continue
        
        clientip, serverip = data.split(':')
        logging.info(f'\rIncoming signal from client {clientip}(source) to {serverip}(dest)')
        clients.append(clientip)

#create a listening thread
listener = threading.Thread(target=listen, daemon=True)
listener.start()
