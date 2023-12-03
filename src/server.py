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


#clients stores strings in form of "ip:port"
clients = []
threads = []
conns = []
lock = threading.Lock()

# create and bind listening socket for clients to send to
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind((hostip, sport))
sock.listen()

logging.info(f'I\'m a signaling server')
# call when the clients list is updated
# send updated client list to all clients on the list
def clients_update():
    clist = ','.join(clients)
    #conn is a socket object
    for conn in conns:
        try:
            conn.send(bytes(clist, encoding='utf-8'))
        except:
            sock_str = socket.getnameinfo(conn.getsockname())
            logging.warning(f'Error sending list to {sock_str}')
    

# listen for client connections
# note: input is not fully sanitized
# waits for <clientip>:<serverip> message format
def listen(conn, addr):
    while True:
        logging.info(f'Recieved ping from {addr}')
        client = str(addr[0]) + ':' + str(addr[1])
        if client not in clients:
            logging.debug(f'Adding client {client} to list..')
            with lock:
                conns.append(conn)
                clients.append(client)
            clients_update()
        #logging.info(f'Sending clientlist: {clients} response to {retaddr}')


# Main thread accepts connections
while True:
    logging.info('Waiting for clients...')
    conn, addr = sock.accept()
    threads.append(threading.Thread(target=listen, args=(conn, addr), daemon=True))
 
sock.close()
