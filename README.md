# Proxy-Server
This is the basic version of Proxy-Server. Run it on a remote server and link the host and port to your device on proxy config to have more control of your network traffic, enhace your network security and reach remote server that are inaccessible for the client's IP address.

# ¿What capabilities does the Proxy-Server basic version have?
Proxy-Server has the most basic capabilities wich are:
  1. Forward network traffic between client device and remote servers.
  2. Hide the client's ip address.
  3. Operate in both application layer protocols http and https (CONNECT http request method).
  4. Enhace network security

# ¿What can I do with Proxy-Server?
This project is public and open source, so users can do several things and add features such as: 
 1. Run the basic version in a remote server and set proxy config at client's device to have a self-controlled server with the above capabilities enhacing the network security.
 2. Filter incomming client connections by the ip address
 3. Loggin
 4. Cache resourses
 5. Filter remote web servers by a criteria (e.g parental control, black list etc)
 6. Link different proxy nodes running different instances in remote servers
 7. Get access to remote servers that are inaccessible with the client's IP address

# About the implementation
It is coded in python with no external dependencies, just with native socket library of python and some others (sys, io etc...).
The implementation is low-level system oriented in terms of network manipulation, even though it is coded in python.
It handles the connection between client's device and proxy-server and between proxy-server and remote servers over TCP protocol in transport layer and IP version 4 in network layer.
The current implementation does not cache, store, read or any similar action, it is specifically performed to redirect the traffic network from the client device to remote server through a proxy layer.
It runs under a single process and is performed to discard usless connections and to avoid blocking functions with multi-threading.
Proxy-Server handles connection through a first HTTP request (after TCP connection) for any method in the case of HTTP protocol, and through CONNECT method in case of HTTPS protocol.

# ¿How can I run it?
You can run it easilly with these simple steps:
  1. Set the host ip address or domain and the port (8080 preferred) in the config.json file (/proxy_server/config.json) of the server where it will be running. Or the LAN host if you're using port forwarding.
  ```
#config.json
{
   "HOST": XXX.XXX.XXX.XXX,
   "PORT": 8080
}
  ```
  2. Run the program
  3. Set the same host ip address or domain and the port in your client's device.
  4. Now you are connected to the remote servers accessed by your applications through a proxy-server.
  5. If you want to terminate the process press enter key on the console. [WARNING] This action is risky because it does not take care of the pending to receive or send data, it just close all the connections both client-proxy and proxy-webserver and ends the process. So be careful with it and make sure your data has been successfully transferred and close the client browsers linked to proxy-server before terminate the process.

# Limitations
Some applications does not connect to the required remote servers through a proxy server even though the connection config of the client's devices is set as an active proxy server. So make sure whether your application uses the proxy server config of the device to connect to the remote servers or not. Some of these applications requires an additional proxy config in the application settings.