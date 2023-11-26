import unittest
import socket
import logging

logging.basicConfig(filename='test_server.log', level=logging.DEBUG)

class BasicServerFunctions(unittest.TestCase):
    def test_message(self):
        logging.debug(f'test_message start')

if __name__ == '__main__':
    unittest.main()