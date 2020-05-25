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


class DatabaseDict:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='stu',
                                  charset='utf8')
        self.cur = self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    def find_mean(self, word):
        sql = "select mean from dict where word=%s;"
        self.cur.execute(sql, word)
        return self.cur.fetchone()

    def select_word(self):
        sql = "select word from dict;"
        self.cur.execute(sql)
        return self.cur.fetchall()


def find_mean(connfd):
    while True:
        db = DatabaseDict()
        data = connfd.recv(1024).decode()
        if data[0] == "W" and data[1] == " ":
            word = data.split(" ", 1)[1]
            if (word,) not in db.select_word():
                noexist = "不存在该单词"
                connfd.send(noexist.encode())
            else:
                mean = db.find_mean(word)[0]
                connfd.send(mean.encode())
            db.close()
        else:
            break


def main():
    s = socket()
    s.bind(('0.0.0.0', 2048))
    s.listen(6)
    signal(SIGCHLD, SIG_IGN)
    while True:
        print("等待客户端连接")
        try:
            connfd, addr = s.accept()
            print(addr, "已连接")
        except KeyboardInterrupt:
            print("断开连接")
            break
        p = Process(target=find_mean, args=(connfd,), daemon=True)
        p.start()


if __name__ == '__main__':
    main()
