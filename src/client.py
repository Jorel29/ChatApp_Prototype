import threading
import socket
import logging
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-cid', dest='cid', default=1, help='set client ID')
parser.add_argument('-pt', dest='port', default=50000, help='set port of client')
parser.add_argument('-ip', dest='host', default='127.0.0.1', help='set host ip')
parser.add_argument('-sip', dest='serverip', default='127.0.0.1', help='set server ip')
parser.add_argument('-servport', dest='serverport', default=130000, help='set server port')

args = parser.parse_args()


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(lineno)d] %(asctime)s.%(msecs)03d %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    handlers=[
        logging.FileHandler(filename=f'./src/logs/client{args.cid}_log.log'),
    ])

sock_host = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

hostname = socket.gethostname()
# keep in mind these may change depending on needs
hostip = socket.gethostbyname(hostname)
peerip = None
serverip = None
sport = 8080
dport = 8081
serverport = 8082

#bind to the ports that the client will always listen on
sock_host.bind((hostip, sport))
sock_server.bind((hostip, serverport))

#Client session
logging.info(f'I\'m client: {hostip} listening on: {sport}')

#recieve messages from the server
def sock_listen():
    while True:
        try:
            data = sock_server.recv(1024).decode(encoding='utf-8', errors='strict')
        except UnicodeDecodeError:
            logging.warning(f'Decode error from incoming message from server')
        logging.info(f'\rlist recieved from {serverip}: {data} \n>')

sock_server_listener = threading.Thread(target=sock_listen, daemon=True)
sock_server_listener.start()

#tell server that the host is ready to recieve client list
sock_server.sendto(f'{hostip}:{serverip}', (serverip, serverport))

#link the host to peer to be able to send and recieve messages
def link_peer(peer, dest):
    logging.info(f'linking to peer : {peer} : {dest}')
    sock_host.sendto(b'0', (peer, dest))



