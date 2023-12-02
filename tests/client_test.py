import unittest
import socket
import logging
import time
logging.basicConfig(
    #filename='server_log.log', 
    level=logging.DEBUG,
    format='[%(lineno)d] %(asctime)s.%(msecs)03d %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    handlers=[
        logging.FileHandler(filename='./tests/logs/client_test_log.log'),
        
    ]
    )
#Socket setup
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 8083))
client1:str = None

sock2 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock2.bind(('127.0.0.1', 8084))
client2:str = None
#Macros
SERVER_ADDR = ('127.0.0.1', 8082)
SERVER_MSG = b'127.0.0.1:127.0.0.1'

class BasicClientFunctions(unittest.TestCase):

    def test_basicsignal_ideal(self):
        logging.debug(f'test_basicsignal')
        test_message_expected = '127.0.0.1:8083'

        sock.sendto(SERVER_MSG, SERVER_ADDR)
        logging.debug(f'Waiting for server...')
        data = sock.recv(1024).decode(encoding='utf-8', errors='strict')

        logging.debug(f'Data recieved: {data}')

        self.assertIn(test_message_expected, data, msg= f'{data} not contained in expected {test_message_expected}')
    

    
if __name__ == '__main__':
    unittest.main()