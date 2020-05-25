"""
author: Lewizo
email: 615905244@qq.com
env: Python3.8
socket tcp
"""
from socket import *
from select import select
import re
import os

s=socket()

s.bind(('0.0.0.0',2048))
s.listen(6)

rlist = [s]
wlist = []
xlist = []

print("等待客户端连接.....")
while True:
    rs, ws, xs = select(rlist, wlist, xlist)
    for r in rs:
        if r is s:
            connfd, addr = r.accept()
            print(addr, "已连接")
            rlist.append(connfd)
        else:
            data=r.recv(1024).decode()
            if data[0]=="P" and data[1]==" ":
                name = data.split(" ", 1)[1]
                f = open('/home/lewizo/PycharmProjects/chatroom/server/' + name, 'wb')
                while True:
                    data=r.recv(1024)
                    if data=="# ".encode():
                        f.close()
                        rlist.remove(r)
                        r.close()
                        break
                    f.write(data)
            if data[0]=="G" and data[1]==" ":
                name = data.split(" ", 1)[1]
                print(name)
                f = open('/home/lewizo/PycharmProjects/chatroom/server/' + name, 'rb')
                while True:
                    data=f.read(1024)
                    if not data:
                        r.send("上传完毕".encode())
                        rlist.remove(r)
                        r.close()
                        break
                    r.send(data)
            if data[0]=="L" and data[1]==" ":
                msg="文件:"
                count=0
                for name,sub_folds,files in os.walk("server"):
                    print(files)
                # for file in files:
                #     msg=msg+file+" "
                r.send(msg.encode())
            if data[0]=="W" and data[1]==" ":
                word = data.split(" ", 1)[1]
                f=open("dict.txt",'r')
                for line in f:
                    if word==line.split(" ",1)[0]:
                        mean=re.split(" +",line,1)[1]
                        r.send(mean.encode())
                        break
                f.close()
                noexist="不存在该单词"
                r.send(noexist.encode())
                rlist.remove(r)
                r.close()
                print("等待客户端连接.....")
