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

import socket
from io import DEFAULT_BUFFER_SIZE
from datetime import datetime
from threading import Thread
from messages import SPACE, WARNING_SHUTDOWN


HOST = None
"""str: IP address or domain of proxy server"""
PORT = None
"""int: Port number of proxy server"""
server_socket = None
"""socket: Socket object for proxy server"""
keep_listening = False
"""boolean: Used for keep listening for new connections through the execution"""
socket_connections = {}
"""dictionary: Socket connections (client-proxy and proxy-remote) store"""

def parse_request(raw_data):
    """
    Parse HTTP request from raw data.
    Parameters:
    bytes: raw_data
    Return:
    tupla: address "(HOST, PORT)"
    boolean: Is method CONNECT
    """
    data = raw_data.decode()
    request_lines = [i.strip() for i in data.splitlines()]
    if -1 == request_lines[0].find('HTTP'):
        raise Exception('Not HTTP protocol')
    method, path, http_version = [line.strip() for line in request_lines[0].split(" ")]
    headers = [i.split(':', 1) for i in request_lines[1:-1]]
    if method == 'CONNECT':
        address = path.split(":")
        return (address[0], int(address[1])), True
    else:
        for header in headers:
            if(header[0] == 'Host'):
                host = header[1].strip()
                if path.startswith('https'):
                    return (host, 443), False
                elif path.startswith('http'):
                    return (host, 80), False
    raise Exception('It has not been possible to get the address from the request')

def connect_to_server(address):
    """
    Create a socket connection with the given address.
    Parameters:
    tupla: address "(HOST, PORT)" 
    """
    remote_server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_server_connection.connect(address)
    print()
    return remote_server_connection

def forwarding_loop(src_conn, dst_conn):
    """
    Loop of data redirection from source connection to destination connection.
    Parameters:
    socket.connection: Source connection socket
    socket.connection: Destination connection socket
    """
    try:
        while keep_listening:
            data = src_conn.recv(DEFAULT_BUFFER_SIZE)
            if data:
                dst_conn.sendall(data)
            else:
                raise Exception('No more data from client')
    except ConnectionResetError:
        print(f'The host has terminated the connection. Details:\n[CONNECTION]: {src_conn}\n{SPACE}')
    except Exception as e:
        print(f'Connection {src_conn} has been closed:\n{e}\n{SPACE}')
    finally:
        src_conn.close()
        dst_conn.close()

def forward_data(client_connection, remote_connection):
    """
    Create two threads where data will be forwarded from client connection to remote server connection and vice versa in loop.
    Parameters:
    socket.connection: Socket connection between client and proxy server.
    socket.connection: Socket connection between proxy server and remote server.
    """
    global socket_connections
    forward_client_to_remote = Thread(target=forwarding_loop, args=[client_connection, remote_connection])
    forward_remote_to_client = Thread(target=forwarding_loop, args=[remote_connection, client_connection])
    forward_client_to_remote.start()
    forward_remote_to_client.start()
    print(f'Forwarding loop between Client {client_connection} and Remote {remote_connection} at {datetime.now()}\n{SPACE}')
    forward_client_to_remote.join()
    forward_remote_to_client.join()
    del socket_connections[str(id(client_connection))]
    del socket_connections[str(id(remote_connection))]

def start_new_connection(client_connection):
    """
    Get remote server address from the first client request and create new connection with it.
    Parameters:
    socket.connection: Socket connection between client and proxy server
    """
    accepted_response = "HTTP/1.1 200 Connection Established\r\n\r\n".encode()
    rejected_response = "HTTP/1.1 400 Bad Request\r\n\r\n".encode()
    remote_server_connection = None

    data = client_connection.recv(DEFAULT_BUFFER_SIZE)
    try:
         address, is_connect_method = parse_request(data)
         print(address)
    except Exception:
         client_connection.sendall(rejected_response)
         client_connection.close()
         print(f'Connection refused because of bad request\nConnection: {client_connection}\n{SPACE}')
         return
    
    remote_server_connection = connect_to_server(address)
    socket_connections[str(id(remote_server_connection))] = remote_server_connection

    if is_connect_method:
        client_connection.sendall(accepted_response)
    else:
        remote_server_connection.sendall(data)

    forward_data(client_connection, remote_server_connection)

def listen_new_connections():
    """
    Listen for new connections from client and accept them in loop while keep_listening is True.
    """
    global server_socket, keep_listening, socket_connections
    while keep_listening:
        try:
            print(f'Listening on {HOST}:{PORT}\n{SPACE}')
            server_socket.listen(1)
            client_connection, client_address = server_socket.accept()
            print(f'Client connected at {datetime.now()}. Address: {client_address}\n{SPACE}')
            socket_connections[str(id(client_connection))] = client_connection
            t = Thread(target=start_new_connection, args=[client_connection])
            t.start()
        except Exception as e:
            print(f'Unexpected exception while listening for new connection\nException: {e}\n{SPACE}')

def shutdown_server_listener(callback):
    """
    Call the given callback function which is a blocking function, and after blockage is released then close all socket connections of client, server proxy and remote server.
    Parameter:
    callback: Function that blocks the code waiting for some event.
    """
    global socket_connections, keep_listening, server_socket
    print(WARNING_SHUTDOWN)
    callback()
    #Close all connections
    for id_connection, connection in socket_connections.items():
        connection.close()
    keep_listening = False
    server_socket.close()
    server_socket

def press_key():
    """
    Wait for enter key press.
    """
    input()