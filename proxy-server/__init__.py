####################################################################
#                                                                  #
#                        [PROXY - SERVER]                          #
#                                                                  #
#------------------------------------------------------------------#
#  Author: Mohamed Mahmoudi (SimoDev98)                            #
#  Github link: github.com/SimoDev98/Proxy-Server                  #
#  Version: Proxy-Server 1.0.0                                     #
#  Licence: Apache 2.0                                             #
#  Copyright Proxy-Server 1.0.0 Mohamed Mahmoudi (SimoDev98)       #
####################################################################


import connection
from sys import exit
from threading import Thread
from json import load
import socket
from messages import INIT_MSG

def main():
    try:
        #Read HOST and PORT from config file:
        with open('config.json', 'r') as file:
            config = load(file)
            connection.HOST = config["HOST"]
            connection.PORT = config["PORT"]
        #Connect socket
        connection.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.server_socket.bind((connection.HOST, connection.PORT))
        print(INIT_MSG)
    except Exception as e:
        print(f'Could not start up proxy server.\nException: {e}')
        exit(1)
    
    t1 = Thread(target=connection.shutdown_server_listener, args=[connection.press_key])
    t1.start()
    connection.keep_listening = True
    connection.listen_new_connections()
    t1.join()
    
    exit(0)

main()