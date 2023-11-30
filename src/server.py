import threading
import socket
import logging

logging.basicConfig(
    #filename='server_log.log', 
    level=logging.DEBUG,
    format='[%(lineno)d] %(asctime)s.%(msecs)03d %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    handlers=[
        logging.FileHandler(filename='./src/logs/server_log.log'),
        logging.StreamHandler()
    ]
    )

# get hostname and ip and set ports
hostname = socket.gethostname()
hostip = '127.0.0.1'
logging.debug(f'hostname: {hostname}, hostip: {hostip}')
sport = 8082
dport = 8083

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
            rawdata, retaddr = sock.recvfrom(1024)
            data = rawdata.decode(encoding='utf-8', errors='strict')
        except:
            logging.warning(f'Decode error from incoming message from a client')
            continue
        
        #Very basic sanitizing 
        try:
            clientip, serverip = data.split(':')
        except:
            logging.warning('Malformed message from client')
            continue
        logging.debug(f'Checking {serverip} != {hostip}')
        if serverip != hostip:
            logging.warning(f'{hostip} does not match dest: {serverip}')
            continue
        logging.debug(f'Checking {clientip} != {retaddr[0]}')
        if clientip != retaddr[0]:
            logging.warning(f'clientip ({clientip}) does not match retaddr ({retaddr})')
            continue


        logging.info(f'Incoming signal from client {clientip}(source) to {serverip}(dest)')
        logging.debug(f'clientlist: {clients} checking if {clientip} is in list...')
        if clientip not in clients:
            logging.debug('Adding clientip to list..')
            clients.append(clientip)
        logging.info(f'Sending clientlist: {clients} response to {clientip}')
        clientlist = ':'.join(clients)
        msg = f'{clientlist}'
        sock.sendto(bytes(msg, encoding='utf-8'), (clientip, dport))
        

# create a listening thread
listener = threading.Thread(target=listen, daemon=True)
listener.start()

while True:
    continue

