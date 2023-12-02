import threading
import socket
import logging
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument('-pt', dest='port', default=50000, help='set port of client')
parser.add_argument('-ip', dest='host', default='127.0.0.1', help='set host ip')
parser.add_argument('-sip', dest='serverip', default='127.0.0.1', help='set server ip')
parser.add_argument('-sp', dest='serverport', default=13000, help='set server port')

args = parser.parse_args()

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
sport = args.serverport
dport = 8083

#clients stores strings in form of "ip:port"
clients = []

# create and bind listening socket for clients to send to
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind((hostip, sport))

logging.info(f'I\'m a signaling server')
# call when the clients list is updated
# send updated client list to all clients on the list
def clients_update():
    clist = ','.join(clients)
    msg = f'{clist}'
    for client in clients:
        ip, port = client.split(':')
        logging.info(f'sending updated {msg} to {ip}:{port}')
        #temporarily send redundantly until TCP is set up 
        sent = sock.sendto(bytes(msg, encoding='utf-8'), (ip, int(port)))
        sent = sock.sendto(bytes(msg, encoding='utf-8'), (ip, int(port)))
        
        #logging.info(f'bytes sent: {sent}')

# listen for client connections
# note: input is not fully sanitized
# waits for <clientip>:<serverip> message format
def listen():
    while True:
        try:
            logging.info('Waiting for clients...')
            rawdata, retaddr = sock.recvfrom(1024)
            data = rawdata.decode(encoding='utf-8', errors='strict')
            # used for rapid testing purposes, please remove after better solution is made
            if 'clear' in data:
                clients.clear()
        except:
            logging.warning(f'Decode error from incoming message from a client')
            continue
        #store client addr
        logging.info(f'Recieved ping from {retaddr}')
        client = str(retaddr[0]) + ':' + str(retaddr[1])
        
        logging.info(f'Incoming signal from client {client}(source)')
        logging.debug(f'clientlist: {clients} checking if {client} is in list...')
        if client not in clients:
            logging.debug('Adding client to list..')
            clients.append(client)
            clients_update()
        #logging.info(f'Sending clientlist: {clients} response to {retaddr}')
        
        

# create a listening thread
listener = threading.Thread(target=listen, daemon=True)
listener.start()

while True:
    continue

