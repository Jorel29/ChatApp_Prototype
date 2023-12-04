import threading
import socket
import logging
import argparse
import time
import queue

parser = argparse.ArgumentParser()

parser.add_argument('-pt', dest='port', default=50000, help='set port of client')
parser.add_argument('-ip', dest='host', default='127.0.0.1', help='set host ip')
parser.add_argument('-sip', dest='serverip', default='127.0.0.1', help='set server ip')
parser.add_argument('-sp', dest='serverport', default=13400, help='set server port')

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
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
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
def conn_accept(conn, addr):
    while True:
        logging.info(f'Recieved ping from {addr}')
        try:
            data = conn.recv(1024).decode()
        except TimeoutError or InterruptedError:
            logging.warning('Connection error, closing connection')
            break
        except:
            logging.warning('Reading data error, closing connection')
            conn.close()
            break
        logging.info(f'UDP Port Recieved {data}')
        client = str(addr[0]) + ':' + data
        if client not in clients:
            logging.debug(f'Adding client {client} to list..')
            with lock:
                conns.append(conn)
                clients.append(client)
            clients_update()
        #logging.info(f'Sending clientlist: {clients} response to {retaddr}')
        time.sleep(0.01)
    #threading.current_thread().join()

def listen():
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=conn_accept, args=(conn, addr), daemon=True)
        thread.start()
        threads.append(thread)
        time.sleep(0.01)

listen_thread = threading.Thread(target=listen, daemon=True)
listen_thread.start()

def keyboard_thread(inputQueue):
    while True:
        input_str = input('->')
        inputQueue.put(input_str)


inputQueue = queue.Queue()
inputThread = threading.Thread(target=keyboard_thread, args=(inputQueue,), daemon=True)
inputThread.start()
# Main thread accepts connections
while True:
    
    if inputQueue.qsize() > 0:
        input_str = inputQueue.get()
        if input_str == 'kill':
            break
    #logging.info('Waiting for clients...')
    
    time.sleep(0.01)
print('Killing server...')
    
