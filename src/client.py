import threading
import socket
import logging

logging.basicConfig(filename='client_log.log', level=logging.DEBUG)

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
        data = sock_server.recv(1024).decode()
        print(f'\rpeer {serverip}: {data} \n>')

sock_server_listener = threading.Thread(target=sock_listen, daemon=True)
sock_server_listener.start()

#tell server that the host is ready to recieve client list
sock_server.sendto(f'{hostip}:{serverip}', (serverip, serverport))

#link the host to peer to be able to send and recieve messages
def link_peer(peer, dest):
    logging.info(f'linking to peer : {peer} : {dest}')
    sock_host.sendto(b'0', (peer, dest))



