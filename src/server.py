import threading
import socket
import logging

logging.basicConfig(
    filename='server_log.log', 
    level=logging.DEBUG,
    format='[%(lineno)d] %(asctime)s %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    )

# get hostname and ip and set ports
hostname = socket.gethostname()
hostip = '127.0.0.1'
logging.debug(f'hostname: {hostname}, hostip: {hostip}')
sport = 8082
dport = 8080

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
            logging.info('Waiting for clients...')
            data = sock.recv(1024).decode(encoding='utf-8', errors='strict')
        except:
            logging.warning(f'Decode error from incoming message from a client')
            continue
        
        #Very basic sanitizing, do not actually do this
        try:
            clientip, serverip = data.split(':')
        except:
            logging.warning('Malformed message from client')
            continue

        logging.info(f'Incoming signal from client {clientip}(source) to {serverip}(dest)')
        clients.append(clientip)
        logging.info(f'Sending response to {clientip}')
        clientlist = ':'.join(clients)
        msg = f'{clientlist}'
        sock.sendto(bytes(msg, encoding='utf-8'), (clientip, 8080))
        

# create a listening thread
listener = threading.Thread(target=listen, daemon=True)
listener.start()

while True:
    continue

