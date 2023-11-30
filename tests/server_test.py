import unittest
import socket
import logging

logging.basicConfig(
    filename='server_test_log.log', 
    level=logging.DEBUG,
    format='[%(lineno)d] %(asctime)s %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%SSSS',
    )
#Socket setup
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 8080))

#Macros
SERVER_ADDR = ('127.0.0.1', 8082)
SERVER_MSG = b'127.0.0.1:127.0.0.1'

class BasicServerFunctions(unittest.TestCase):

    def test_single_client_message(self):
        logging.debug(f'test_single_client_message start')
        test_message_expected = '127.0.0.1'

        sock.sendto(SERVER_MSG, SERVER_ADDR)
        logging.debug(f'Waiting for server...')
        data = sock.recv(1024).decode(encoding='utf-8', errors='strict')

        logging.debug(f'Data recieved: {data}')

        self.assertIn(test_message_expected, data, msg= f'{data} not contained in expected {test_message_expected}')
 
    def 
        

if __name__ == '__main__':
    unittest.main()