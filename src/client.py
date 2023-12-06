import threading
import socket
import logging
import argparse
import queue
import time
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

parser = argparse.ArgumentParser()

parser.add_argument('-cid', dest='cid', default=1, help='set client ID')
parser.add_argument('-pt', dest='port', default=50000, help='set port of client')
parser.add_argument('-ip', dest='host', default='127.0.0.1', help='set host ip')
# need to rename these
parser.add_argument('-sip', dest='serverip', default='127.0.0.1', help='set server ip to listen on')
parser.add_argument('-sp', dest='serverport', default=13000, help='set server port that client will recieve data')
parser.add_argument('-ssip', dest='sigserverip', default='127.0.0.1', help='set ip of signal server')
parser.add_argument('-ssp', dest='sigport', default=13400, help='set port of signal server to recieve data')

args = parser.parse_args()


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(lineno)d] %(asctime)s.%(msecs)03d %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    handlers=[
        logging.FileHandler(filename=f'./src/logs/client{args.cid}_log.log'),
    ])

#GUI
app = QApplication([])
text_area = QPlainTextEdit()
text_area.setFocusPolicy(Qt.FocusPolicy.NoFocus)
message = QLineEdit()
layout = QVBoxLayout()
peers = QComboBox()
layout.addWidget(peers)
layout.addWidget(text_area)
layout.addWidget(message)
window = QWidget()
window.setLayout(layout)
window.show()


hostname = socket.gethostname()
# keep in mind these may change depending on needs
hostip = args.host
serverip = args.serverip
sport = int(args.port)
host_addr = (hostip, sport)
serverport = int(args.serverport)
#address of server
sigip = args.sigserverip
sigport = int(args.sigport)
signalserver = (sigip, sigport)
peerip = None
dport = 8081
peer = None
# Create and bind the UDP socket
sock_host = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock_host.bind((hostip, sport))

# Create and bind TCP socket
sock_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock_server.bind((serverip, serverport))

#Client session
logging.info(f'I\'m client: {hostip} listening on: {sport}')

# dict of addresses that client can connect to
# format: clientid: tuple(ip, port)
clients = dict()

active_conn = False
cid = 1
# Check into server that the host is ready to recieve client list
def removeaddr(addr):
    ip, port = addr.split(':')
    index = peers.findText(addr)
    peers.removeItem(index)
    keytoremove = None
    for key, value in clients.items():
        if value[0]==ip and value[1] == int(port):
            keytoremove = key 
    clients.pop(keytoremove)
    logging.debug(f'deleted {addr}')

def convert_to_addrs(list):
    global cid
    for string in list:
        ip, port = string.split(':')
        addr = (ip, int(port))
        clients[cid] = addr
        if host_addr != addr:
            peers.addItem(string, addr)
        cid += 1
    logging.debug(f'updated clients dict: {clients}')
#recieve messages from the server
def sock_listen():
    while True:
        try:
            logging.info('Waiting for server updates...')
            data = sock_server.recv(1024).decode(encoding='utf-8', errors='strict')
        except UnicodeDecodeError:
            logging.warning(f'Decode error from incoming message from server')
        except ConnectionError:
            logging.warning('Lost Connection to server')
        logging.info(f'list recieved from server: {data} \n>')
        if 'R' in data:
            temp = data.split(' ')
            removeaddr(temp[1])
            continue
        clist = data.split(',')
        convert_to_addrs(clist)

sock_server.connect(signalserver)
msg = f'{sport}'
sock_server.send(bytes(msg, encoding='utf-8'))
sock_server_listener = threading.Thread(target=sock_listen, daemon=True)
sock_server_listener.start()


def reply_isvalid(reply):
    if len(reply) > 1:
        return False
    return ('Y' in reply) or ('y' in reply) or ('N' in reply) or ('n' in reply)

#link the host to peer to be able to send and recieve messages
def link_peer(addr, reply):
    logging.info(f'linking to peer : {addr}')
    global peer
    if 'Y' in reply or 'y' in reply:
        peer = addr

    sock_host.sendto(bytes(reply, encoding='utf-8'), peer)
    
# This thread is created after the clients dict length is > 1
def conn_listen():
    global peer
    global active_conn
    while True:
        try:
            logging.info('Ready to recieve messages')
            rawdata, retaddr = sock_host.recvfrom(1024)
            data = rawdata.decode(encoding='utf-8', errors='strict')
        except:
            logging.warning('Error recieving data from sock_host')
            continue
        # check if retaddr is actually from a valid client
        if retaddr not in clients.values():
            continue
        # if active connection, print out peer message data
        
        print(f'\r{retaddr[0]}.{retaddr[1]}:-> {data}')
        incoming_msg = f'{retaddr[0]}.{retaddr[1]}:-> {data}'
        text_area.appendPlainText(incoming_msg)
        
        time.sleep(0.01)
        
            
# Create a connection listener thread
sock_client_listener = threading.Thread(target=conn_listen, daemon=True)
sock_client_listener.start()



def select_peer():
    #select a peer
    global peer
    peer = peers.currentData()
    logging.info(f'Current Peer: {peer}')

def send_message():
    #send out a typed message to selected peer
    msg = message.text()
    logging.info(f'Sending Message to {peer}: {message}')
    sock_host.sendto(bytes(msg, encoding='utf-8'), peer)
    message.clear()

peers.currentIndexChanged.connect(select_peer)
message.returnPressed.connect(send_message)
app.exec()

print('Killing client...')    
    
