# %%
# package import
import os
import time
import subprocess
import socket
import sys
import logging
import pexpect
from connect_vpn import is_connectable
# env
from dotenv import load_dotenv

load_dotenv()

NAS_SERVER=os.environ.get('NAS_SERVER')
NAS_ID=os.environ.get('NAS_ID')
NAS_PASSWORD=os.environ.get('NAS_PASSWORD')
REMOTE_DIR=os.environ.get('REMOTE_DIR')
LOCAL_DIR=os.environ.get('LOCAL_DIR')
def wait_password(name, host):
    pw_str = '%s@%s\'s password:' % (name, host)
    print(pw_str)
    return pw_str

# sshfs를 활용한 sftp 폴더 마운트가 되어있는 지 확인
def is_mounted():
    result = subprocess.run(["mount"], stdout=subprocess.PIPE, text=True)
    if f'{NAS_ID}@{NAS_SERVER}' in result.stdout:
        print('connected: ', f'{NAS_ID}@{NAS_SERVER}')
        return True
    else:
        return False
    
# %%
# sshfs를 활용한 sftp 폴더 마운트
def mount():
    if is_mounted() == False:
        mount_str = f'sshfs -o reconnect {NAS_ID}@{NAS_SERVER}:{REMOTE_DIR} {LOCAL_DIR}  -ovolname={NAS_ID}@{NAS_SERVER}'
        print(f'mount_str:{mount_str}')
        if is_connectable(NAS_SERVER,22) == True:
            child = pexpect.spawn('bash', args=['-c', "trap '' HUP; " + mount_str])
            child.expect(wait_password(NAS_ID,NAS_SERVER))
            child.sendline(NAS_PASSWORD)
            child.expect(pexpect.EOF)


if __name__ == '__main__':
    if is_connectable(NAS_SERVER,22) == True:
        print('nas connected')
        mount()
    else:
        print('nas not connected')
