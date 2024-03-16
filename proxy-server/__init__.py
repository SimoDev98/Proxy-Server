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


import proxy_server
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
            proxy_server.HOST = config["HOST"]
            proxy_server.PORT = config["PORT"]
        #Connect socket
        proxy_server.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_server.server_socket.bind((proxy_server.HOST, proxy_server.PORT))
        print(INIT_MSG)
    except Exception as e:
        print(f'Could not start up proxy server.\nException: {e}')
        exit(1)
    
    t1 = Thread(target=proxy_server.shutdown_server_listener, args=[proxy_server.press_key])
    t1.start()
    t2 = Thread(target=proxy_server.discard_disconnected_sockets, args=[20])
    proxy_server.keep_listening = True
    proxy_server.listen_new_connections()
    t1.join()
    t2.join()
    
    exit(0)

main()