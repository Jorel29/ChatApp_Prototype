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
        logging.FileHandler(filename='./tests/logs/server_test_log.log'),
        
    ]
    )
sock_reset = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Socket setup
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 8083))
client1:str = None

sock2 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock2.bind(('127.0.0.1', 8084))
client2:str = None
#Macros
SERVER_ADDR = ('127.0.0.1', 13000)
SERVER_MSG = b'127.0.0.1:127.0.0.1'

class BasicServerFunctions(unittest.TestCase):

    def tearDown(self) -> None:
        sock.sendto(b'clear', SERVER_ADDR)
        return super().tearDown()
    def test_basicsignal_ideal(self):
        logging.debug(f'test_basicsignal')
        test_message_expected = '127.0.0.1:8083'

        sock.sendto(SERVER_MSG, SERVER_ADDR)
        logging.debug(f'Waiting for server...')
        data = sock.recv(1024).decode(encoding='utf-8', errors='strict')

        logging.debug(f'Data recieved: {data}')

        self.assertIn(test_message_expected, data, msg= f'{data} not contained in expected {test_message_expected}')
    
    #test tries to crash the server with malformed input
    def test_basicsignal_malformed(self):
        logging.debug(f'test_basicsignal_malformed')
        expected = '127.0.0.1:8083'
        #Send a malformed message, then a correct one
        sock.sendto(b'Hello Server!', SERVER_ADDR)
        logging.debug('Sending correctly formed message...')

        sock.sendto(SERVER_MSG, SERVER_ADDR)
        logging.debug('Message sent, Waiting for server...')
        data = sock.recv(1024).decode(encoding='utf-8', errors='strict')

        logging.debug(f'Data recieved: {data}')

        self.assertIn(expected, data, msg= f'{data} not contained in expected {expected}')

    #next two tests try to crash the server with malformed ips
    def test_basicsignal_badserverip(self):
        logging.debug('test_basicsignal_badserverip')
        expected = '127.0.0.1:8083'
        message = b'127.0.0.1:10.0.0.1'
        
        logging.debug('Sending improper ip message')
        sock.sendto(message, SERVER_ADDR)
        
        logging.debug('Sending proper ip message')
        sock.sendto(SERVER_MSG, SERVER_ADDR)
        logging.debug('Message sent, Waiting for server...')
        data = sock.recv(1024).decode(encoding='utf-8', errors='strict')

        logging.debug(f'Data recieved: {data}')

        self.assertIn(expected, data, msg= f'{data} not contained in expected {expected}')

    def test_basicsignal_badclientip(self):
        logging.debug('test_basicsignal_badip')
        expected = '127.0.0.1:8083'
        message = b'127.0.0.2:127.0.0.1'

        logging.debug('Sending improper ip message')
        sock.sendto(message, SERVER_ADDR)
        
        logging.debug('Sending proper ip message')
        sock.sendto(SERVER_MSG, SERVER_ADDR)
        logging.debug('Message sent, Waiting for server...')
        data = sock.recv(1024).decode(encoding='utf-8', errors='strict')

        logging.debug(f'Data recieved: {data}')

        self.assertIn(expected, data, msg= f'{data} not contained in expected {expected}')

    def test_multiclient_nominal(self):

        sock.sendto(b'0', SERVER_ADDR)

        sock2.sendto(b'0', SERVER_ADDR)
        
        data = sock.recv(1024).decode()
        data2 = sock2.recv(1024).decode()
        
        self.assertIn('127.0.0.1:8083', data, msg=f'client not found in data: {data}')
        self.assertIn('127.0.0.1:8084', data, msg=f'client not found in data: {data}')

        self.assertIn('127.0.0.1:8083', data2, msg=f'client not found in data: {data2}')
        self.assertIn('127.0.0.1:8084', data2, msg=f'client not found in data: {data2}')
if __name__ == '__main__':
    unittest.main()