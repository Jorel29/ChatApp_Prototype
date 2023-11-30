import unittest
import socket
import logging

logging.basicConfig(
    filename='server_test_log.log', 
    level=logging.DEBUG,
    format='[%(lineno)d] %(asctime)s.%(msecs)03d %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    )
#Socket setup
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 8080))

#Macros
SERVER_ADDR = ('127.0.0.1', 8082)
SERVER_MSG = b'127.0.0.1:127.0.0.1'

class BasicServerFunctions(unittest.TestCase):

    def test_basicsignal_ideal(self):
        logging.debug(f'test_basicsignal')
        test_message_expected = '127.0.0.1'

        sock.sendto(SERVER_MSG, SERVER_ADDR)
        logging.debug(f'Waiting for server...')
        data = sock.recv(1024).decode(encoding='utf-8', errors='strict')

        logging.debug(f'Data recieved: {data}')

        self.assertIn(test_message_expected, data, msg= f'{data} not contained in expected {test_message_expected}')
 
    def test_basicsignal_malformed(self):
        logging.debug(f'test_basicsignal_malformed')
        expected = '127.0.0.1'
        #Send a malformed message, then a correct one
        sock.sendto(b'Hello Server!', SERVER_ADDR)
        logging.debug('Sending correctly formed message...')

        sock.sendto(SERVER_MSG, SERVER_ADDR)
        logging.debug('Message sent, Waiting for server...')
        data = sock.recv(1024).decode(encoding='utf-8', errors='strict')

        logging.debug(f'Data recieved: {data}')

        self.assertIn(expected, data, msg= f'{data} not contained in expected {expected}')

    def test_basicsignal_badserverip(self):
        logging.debug('test_basicsignal_badip')
        expected = '127.0.0.1'
        message = b'127.0.0.2:10.0.0.1'

        logging.debug('Sending improper ip message')
        sock.sendto(message, SERVER_ADDR)
        
        logging.debug('Sending proper ip message')
        sock.sendto(SERVER_MSG, SERVER_ADDR)
        logging.debug('Message sent, Waiting for server...')
        data = sock.recv(1024).decode(encoding='utf-8', errors='strict')

        logging.debug(f'Data recieved: {data}')

        self.assertIn(expected, data, msg= f'{data} not contained in expected {expected}')




if __name__ == '__main__':
    unittest.main()