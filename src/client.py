import threading
import socket
import logging
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-cid', dest='cid', default=1, help='set client ID')
parser.add_argument('-pt', dest='port', default=50000, help='set port of client')
parser.add_argument('-ip', dest='host', default='127.0.0.1', help='set host ip')
# need to rename these
parser.add_argument('-sip', dest='serverip', default='127.0.0.1', help='set server ip to listen on')
parser.add_argument('-sp', dest='serverport', default=13000, help='set server port')
parser.add_argument('-ssip', dest='sigserverip', default='127.0.0.1', help='set ip of signal server')
parser.add_argument('-ssp', dest='sigport', default=13400, help='set port of signal server')

args = parser.parse_args()


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(lineno)d] %(asctime)s.%(msecs)03d %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    handlers=[
        logging.FileHandler(filename=f'./src/logs/client{args.cid}_log.log'),
        logging.StreamHandler()
    ])




hostname = socket.gethostname()
# keep in mind these may change depending on needs
hostip = args.host
serverip = args.serverip
sport = int(args.port)
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


# Check into server that the host is ready to recieve client list


def convert_to_addrs(list):
    cid = 1
    for string in list:
        ip, port = string.split(':')
        
        clients[cid] = (ip, int(port))
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
        logging.info(f'list recieved from server: {data} \n>')

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
    active_conn = False
    while True:
        try:
            rawdata, retaddr = sock_host.recvfrom(1024)
            data = rawdata.decode(encoding='utf-8', errors='strict')
        except:
            logging.warning('Error recieving data from sock_host')
            continue
        # check if retaddr is actually from a valid client
        if retaddr not in clients.values():
            continue
        # if active connection, print out peer message data
        if active_conn == True:
            print(f'{peer[0]}.{peer[1]}:-> {data}')
            continue
        
        # Check if data is about accepting a peer request 
        if 'y' in data or 'Y' in data:
            active_conn = True
            peer = retaddr
            continue

        if 'n' in data or 'N' in data:
            active_conn = False
            continue

        # reply to accept incoming connection request
        reply = input(f'Would you like to connect to peer {retaddr[0]}.{retaddr[1]}(Y/N)?')
        
        while(not reply_isvalid(reply)):
            print('Reply must be 1 character Y or N')
            reply = input(f'Would you like to connect to peer {retaddr[0]}.{retaddr[1]}(Y/N)?')
        link_peer(retaddr, reply)
            
# Create a connection listener thread
sock_client_listener = threading.Thread(target=conn_listen, daemon=True)
sock_client_listener.start()

def print_peers():
    for pid, peer in clients.items():
        if hostip in peer and sport in peer: 
            continue
        else:
            print(f'ID: {pid}, ADDR: {peer}')
     
# main thread 
while True:

    if(len(clients) > 1):
        print(f'PEERS :')
        print_peers()
        cmd = input('Choose a peer ID:')
        if int(cmd) > len(clients) or int(cmd) < 1 or args.cid in cmd:
            print('INVALID INPUT, TRY AGAIN')
            continue
        
    continue
    
