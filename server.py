# -*- coding: utf-8 -*-#
import socket
import struct
import json
import subprocess

phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 避免出现io占用情况
phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

phone.bind(('127.0.0.1', 8080))

phone.listen(5)

while True:
    conn, addr = phone.accept()
    while True:
        cmd = conn.recv(1024)
        # 回收无效套接字，这里因为是在linux上跑ssh，所以就没必要去捕获windows下的ConnectionResetError了
        if not cmd:
            break

        res = subprocess.Popen(cmd.decode('utf-8'),
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        err = res.stderr.read()

        if err:
            back_msg = err
        else:
            back_msg = res.stdout.read()

        headers = {'data_size': len(back_msg)}
        head_json = json.dumps(headers)
        head_json_bytes = bytes(head_json, encoding='utf-8')

        # 先发json header长度
        conn.send(struct.pack('i', len(head_json_bytes)))
        # 再发送json header
        conn.send(head_json_bytes)
        # 再发送真实数据
        conn.sendall(back_msg)

    conn.close()
