"""
author: Lewizo
email: 615905244@qq.com
env: Python3.8
socket udp & tcp & multiprocessing
"""
from socket import *
from multiprocessing import *
import chatroom_ui
import sys

def menu(us):
    print('''        =============== 聊天室菜单 ===============   
        1 登录                           				    
        2 注册账号                             				    
        3 更改账号昵称 
        4 修改密码
        5 更改头像(暂未开放)
        6 上传共享文件
        7 下载共享文件    
        8 查看共享文件	
        9 在线词典			                    				    
        0 退出聊天室                                 			   	    
        ========================================   ''')
    while True:
        select=input("请选择 >>")
        if select=="1":
            name=log_in(us)
            return name
        if select=="2":
            regist(us)
        if select=="3":
            change_name(us)
        if select=="4":
            pass #change_password(us)
        if select=="5":
            pass #change_image(us)
        if select=="6":
            put_file()
        if select=="7":
            get_file()
        if select=="8":
            look_file()
        if select=="9":
            find_word()
        if select=="0":
            sys.exit("退出")

def log_in(us):
    while True:
        name = input("输入昵称：")
        password = input("输入密码：")
        msg="L "+name+" "+password
        us.sendto(msg.encode(), ('127.0.0.1', 2048))
        data, addr = us.recvfrom(1024)
        print(data.decode())
        if data.decode()=="进入聊天室":
            return name

def regist(us):
    while True:
        name=input("输入昵称：")
        password = input("输入密码：")
        msg="R "+name+" "+password
        us.sendto(msg.encode(), ('127.0.0.1', 2048))
        data, addr = us.recvfrom(1024)
        print(data.decode(),end="")
        if data.decode()=="创建成功！":
            break

def change_name(us):
    while True:
        name=input("输入需要修改的昵称：")
        password = input("输入密码：")
        newname=input("输入新的昵称：")
        msg="E "+name+" "+password+" "+newname
        us.sendto(msg.encode(), ('127.0.0.1', 2048))
        data, addr = us.recvfrom(1024)
        print(data.decode(),end="")
        if data.decode()=="修改成功":
            break

def send_message(name,us):
    while True:
        try:
            word=input(name+">>")
        except KeyboardInterrupt:
            word="exit"
        if word=="exit":
            msg="Q "+name
            us.sendto(msg.encode(), ('127.0.0.1', 2048))
            sys.exit("退出聊天室")
        msg = "C " + name + " " + word
        us.sendto(msg.encode(),('127.0.0.1',2048))

def get_message(name,us):
    while True:
        data, addr = us.recvfrom(1024)
        print("\n"+data.decode()+"\n"+name+">>",end="")

def put_file():
    ts = socket()
    ts.connect(('localhost', 2048))
    name = input("输入要上传的文件名称：")
    msg="P "+name
    ts.send(msg.encode())
    f = open('/home/lewizo/PycharmProjects/chatroom/client/' + name, 'rb')
    while True:
        data=f.read(1024)
        if not data:
            print("上传完毕")
            ts.send("# ".encode())
            break
        ts.send(data)
    f.close()
    ts.close()

def get_file():
    ts = socket()
    ts.connect(('localhost', 2048))
    name=input("输入要下载的文件名称：")
    msg="G "+name
    ts.send(msg.encode())
    f=open('/home/lewizo/PycharmProjects/chatroom/client/'+name,'wb')
    while True:
        data = ts.recv(1024)
        if data == "上传完毕".encode():
            print(data.decode())
            break
        f.write(data)
    f.close()
    ts.close()

def look_file():
    ts = socket()
    ts.connect(('localhost', 2048))
    ts.send("L ".encode())
    list=ts.recv(1024)
    print(list.decode())

def find_word():
    ts = socket()
    ts.connect(('localhost', 2048))
    while True:
        word=input("输入单词：")
        if word=="exit":
            break
        msg="W "+word
        ts.send(msg.encode())
        mean=ts.recv(1024)
        print(mean.decode())

def main():
    us=socket(AF_INET,SOCK_DGRAM)
    name = menu(us)
    p_get=Process(target=get_message,args=(name,us),daemon=True)
    p_get.start()
    send_message(name, us)
    us.close()

if __name__=='__main__':
    main()