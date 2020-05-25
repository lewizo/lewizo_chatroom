"""
author: Lewizo
email: 615905244@qq.com
env: Python3.8
socket udp
"""
from socket import *
import pymysql


class Database:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='stu',
                                  charset='utf8')
        self.cur = self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    def insert(self, exe):
        sql = "insert into chatroom (name,password,address,port) values (%s,%s,%s,%s);"
        self.cur.execute(sql, exe)
        self.db.commit()

    def select_name(self):
        self.cur.execute("select name from chatroom;")
        return self.cur.fetchall()

    def online_addr(self):
        self.cur.execute("select address,port from chatroom where online=1;")
        return self.cur.fetchall()

    def online_name(self):
        self.cur.execute("select name from chatroom where online=1;")
        return self.cur.fetchall()

    def name_password(self, name):
        sql = "select password from chatroom where name=%s;"
        self.cur.execute(sql, name)
        return self.cur.fetchone()

    def change_addr(self, address, port, name):
        self.cur.execute("update chatroom set address='%s',port=%s where name='%s'" % (address, port, name))
        self.db.commit()

    def change_online(self, online, name):
        self.cur.execute("update chatroom set online=%s where name='%s'" % (online, name))
        self.db.commit()

    def change_name(self, newname, name):
        self.cur.execute("update chatroom set name='%s' where name='%s'" % (newname, name))
        self.db.commit()


def main():
    s = socket(AF_INET, SOCK_DGRAM)  # 创建udp套接字
    s.bind(("localhost", 2048))  # 绑定
    print("服务器开启")
    while True:
        db = Database()
        tuple_name = db.select_name()
        online_addr = db.online_addr()
        online_name = db.online_name()
        print(online_name)
        data, addr = s.recvfrom(1024)
        word = data.decode()
        if word[0] == "L" and word[1] == ' ':
            name = word.split(" ", 2)[1]
            password = word.split(" ", 2)[2]
            if (name,) not in tuple_name:
                s.sendto("不存在该账号".encode(), addr)
            elif password != db.name_password(name)[0]:
                s.sendto("密码错误".encode(), addr)
            else:
                s.sendto("进入聊天室".encode(), addr)
                db.change_addr(addr[0], addr[1], name)
                db.change_online(1, name)
                message = name + " 进入聊天室"
                print(message)
                for addr in online_addr:
                    s.sendto(message.encode(), addr)
        if word[0] == "R" and word[1] == ' ':
            name = word.split(" ", 2)[1]
            password = word.split(" ", 2)[2]
            if (name,) not in tuple_name:
                exe = [name, password, addr[0], addr[1]]
                db.insert(exe)
                print("添加用户", addr, "：", name)
                s.sendto("创建成功！".encode(), addr)
            else:
                s.sendto("已存在该昵称，请重新".encode(), addr)
        if word[0] == 'C' and word[1] == ' ':
            message = word.split(" ", 2)[1] + "：" + word.split(" ", 2)[2]
            for addr in online_addr:
                s.sendto(message.encode(), addr)
            print(message)
        if word[0] == 'Q' and word[1] == ' ':
            name = word.split(" ", 1)[1]
            if (name,) in online_name:
                db.change_online(0, name)
                message = word.split(" ", 1)[1] + " 退出聊天室"
                print(message)
                for addr in online_addr:
                    s.sendto(message.encode(), addr)
        if word[0] == 'E' and word[1] == ' ':
            name = word.split(" ", 3)[1]
            password = word.split(" ", 3)[2]
            newname = word.split(" ", 3)[3]
            rightpw = db.name_password(name)[0]
            if (name,) not in tuple_name:
                s.sendto("不存在该账号,请重新".encode(), addr)
            elif password != rightpw:
                s.sendto("密码错误，请重新".encode(), addr)
            else:
                db.change_name(newname, name)
                s.sendto("修改成功".encode(), addr)
                print("用户", name, "将昵称修改为：", newname)
        db.close()


if __name__ == '__main__':
    main()
