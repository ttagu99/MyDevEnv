# %%
'''
인터넷 접속이 되어있는지 확인,
접속 되어 있으면  vpn 연결,
'''
# package import
import os
import time
import subprocess
import socket
import sys
import logging
import pexpect
# env
from dotenv import load_dotenv
load_dotenv()



# 인터넷 접속이 되어있는지 확인
def check_internet():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

# vpn 내부 ip 확인
def is_connectable(ip, port):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()
        

        
# vpn 연결
def connect_vpn(ip, port, username, password, cert):
    # vpn 연결
    connect_str = f'sudo openfortivpn {ip}:{port} -u {username} --trusted-cert {cert}'
    print(f'connect_str:{connect_str}')
    child = pexpect.spawn(connect_str)
    
    index = child.expect(['Password:', 'VPN account password:', pexpect.EOF, pexpect.TIMEOUT])
    if index == 0:
        print(f'password:{password}')
        child.sendline(password)  
    index = child.expect(['Password:', 'VPN account password:', pexpect.EOF, pexpect.TIMEOUT])
    if index == 1:
        print(f'VPN account password:{username}')
        child.sendline(username)
    return child
        
    # print('connecting...')
    # child.wait()
    
        
# python mac os에서 

# %%
# # main
if __name__ == '__main__':
    VPN_SERVER=os.environ.get('VPN_SERVER')
    VPN_USER=os.environ.get('VPN_USER')
    VPN_PORT=os.environ.get('VPN_PORT')
    VPN_CERT_TOKEN=os.environ.get('VPN_CERT_TOKEN')
    LOCAL_DIR=os.environ.get('LOCAL_DIR')
    PASSWORD=os.environ.get('PASSWORD')
    NAS_SERVER=os.environ.get('NAS_SERVER')
    NAS_ID=os.environ.get('NAS_ID')
    NAS_PASSWORD=os.environ.get('NAS_PASSWORD')
    REMOTE_DIR=os.environ.get('REMOTE_DIR')
    
    connect_str = f'sudo openfortivpn {VPN_SERVER}:{VPN_PORT} -u {VPN_USER} --trusted-cert {VPN_CERT_TOKEN}'
    while True:
        if is_connectable(NAS_SERVER,22) == True:
            print('vpn connected')
            time.sleep(10)
        else:
            if check_internet() == True:
                child = connect_vpn(VPN_SERVER, VPN_PORT, VPN_USER, PASSWORD, VPN_CERT_TOKEN)
            else:
                print('internet not connected')
                time.sleep(10)         
        time.sleep(1)
        
