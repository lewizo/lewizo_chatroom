"""
author: Lewizo
email: 615905244@qq.com
env: Python3.8
socket tcp
"""
from socket import *
from multiprocessing import *
from signal import *
import pymysql

class Database_dict:
    def __init__(self):
        self.db=pymysql.connect(host='localhost',port=3306,user='root',password='123456',database='stu',charset='utf8')
        self.cur=self.db.cursor()
    def close(self):
        self.cur.close()
        self.db.close()
    def find_mean(self,word):
        sql = "select mean from dict where word=%s;"
        self.cur.execute(sql, word)
        return self.cur.fetchone()
    def select_word(self):
        sql = "select word from dict;"
        self.cur.execute(sql)
        return self.cur.fetchall()

def find_mean(s):
    connfd, addr = s.accept()
    print(addr, "已连接")
    while True:
        db = Database_dict()
        data = connfd.recv(1024).decode()
        if data[0] == "W" and data[1] == " ":
            word = data.split(" ", 1)[1]
            if (word,) not in db.select_word():
                noexist = "不存在该单词"
                connfd.send(noexist.encode())
            else:
                mean = db.find_mean(word)[0]
                connfd.send(mean.encode())
            print("等待客户端连接.....")
            db.close()

def main():
    s = socket()
    s.bind(('0.0.0.0', 2048))
    s.listen(6)
    print("等待客户端连接")
    p=Process(target=find_mean,args=(s,),daemon=True)
    p.start()


if __name__=='__main__':
    main()