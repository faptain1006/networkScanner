import os
import platform
import socket 
import ipaddress
from datetime import datetime

# input the Network 
net = input("Enter the Network Address: ")

# using the ipaddress library get the ipv4 value of the input
net = ipaddress.IPv4Network(net, strict=False)

# thru the CIDR notation, get the network and the broadcast IPs
start_ip = net.network_address
end_ip = net.broadcast_address

# get the current date time
t1 = datetime.now()

# select the mode
mode = input("Enter mode [ICMP] or [TCP]: ")


if mode == "ICMP": # Ping sweeping
    oper = platform.system()

    # choose the ping flag to use depending on the current OS    
    if (oper == "Windows"):
        ping_command = "ping -n 1 "
    elif (oper == "Linux"):
        ping_command = "ping -c 1 "
    else :
        ping_command = "ping -c 1 "
        t1 = datetime.now()
        print ("Scanning in Progress:")

    # sweep the ping thru the IPs on the given range 
    for ip in net.hosts():
        addr = str(ip)
        comm = ping_command + addr
        response = os.popen(comm)
        
        # process the response (print live IPs only)
        result = response.read()
        if "Sent = 1, Received = 1" in result:
            print(f"{addr} is live")   


    # get the total scanning time   
    t2 = datetime.now()
    total = t2 - t1
    print ("Scanning completed in: " , total)
    
elif mode == "TCP": # Port scanning
    # get the input port from the user
    port = int(input("Please enter the port: "))
    print("Scanning...")

    # create a scan function using socket library
    def scan(addr):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((addr,port))
        if result == 0:
            return 1
        else :
            return 0
    # scan the ip range in net.hosts() and print if socket is live
    for ip in net.hosts():
        if scan(str(ip)):
            print(f"{ip}:{port} is live")      

    # get the total scanning time
    t2 = datetime.now()
    total = t2 - t1
    print ("Scanning completed in: " , total)

else: 
    print('Input error')
