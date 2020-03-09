# -*- coding: utf-8 -*-#
from socket import *
import struct
import json

ip_port = ('127.0.0.1', 8080)
client = socket(AF_INET, SOCK_STREAM)
client.connect(ip_port)

while True:
    cmd = input('>>: ')
    if not cmd:
        continue
    client.send(bytes(cmd, encoding='utf-8'))

    # 收json header长度
    head = client.recv(4)
    head_json_len = struct.unpack('i', head)[0]
    # 收json header
    head_json = json.loads(client.recv(head_json_len).decode('utf-8'))
    # 拿到真实数据长度
    data_len = head_json['data_size']

    recv_size = 0
    recv_data = b''
    # 开始接收数据，直到收完为止
    while recv_size < data_len:
        recv_data += client.recv(1024)
        # 收集长度，考虑到以后打日志可能会用
        recv_size += len(recv_data)

    print(recv_data.decode('utf-8'))
