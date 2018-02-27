#!/usr/bin/python3
# -*-coding:utf-8-*-

import tkinter
import threading
import socket


class ListenThread(threading.Thread):
    """监听线程"""
    def __init__(self, edit, server):
        threading.Thread.__init__(self)
        self.edit = edit  # 保存窗口的多行文本
        self.server = server  # 保存server socket

    def run(self):  # 重写run
        while True:
            try:
                client, addr = self.server.accept()  # 接受client socket
                self.edit.insert(tkinter.END, "连接来自:{}\n".format(addr))  # 向文本框输入状态
                while True:
                    data = client.recv(1024)  #
                    msg = "收到数据:{}\n".format(data.decode())
                    self.edit.insert(tkinter.END, msg)  # 向文本框输出状态
                    client.send((str("I GOT :{}".format(data.decode()))).encode())  # 发送数据
                    # client.close()
                    # self.edit.insert(tkinter.END, "关闭客户端\n")  # 向文本框输出状态
                    if data.decode().strip() == "q":
                        self.edit.insert(tkinter.END, "关闭客户端\n")  # 向文本框输出状态
                        client.close()
                        break  # 退出
            except Exception as e:
                print(e)
                self.edit.insert(tkinter.END, "关闭连接\n")  # 异常关闭连接
                break
            break
            # client.close()  # 关闭服务端


class Control(threading.Thread):  # 继承Thread
    """控制线程"""
    def __init__(self, edit):  # 重写__init__
        threading.Thread.__init__(self)  # 继承Thread.__init__
        self.edit = edit  # edit是传进来文本框对象    保存窗口的多行文本框
        self.event = threading.Event()  # 创建event对象
        self.event.clear()  # 清除event标志

    def run(self):  # 重写run方法
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建server socket
        server.bind(("", 7788))  # 绑定IP和端口
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 设定地址复用
        server.listen(128)  # 监听
        self.edit.insert(tkinter.END, "正在等待连接\n")  # 给窗口的文本框传如数据

        self.Li = ListenThread(self.edit, server)  # 创建监听对象,收发数据线程,传入窗口文本框对象和,server socket
        self.Li.setDaemon(True)  # 设定主线成结束后,子线程结束
        self.Li.start()  # 启动监听线程
        self.event.wait()  # 进入等待状态  event是啥功能
        server.close()  # 关闭套接字

    def stop(self):
        self.event.set()


class Window(object):
    """创建显示窗口"""
    def __init__(self, root):
        self.root = root
        self.butlisten = tkinter.Button(root, text="开始监听", command=self.Listen)  # 创建开始监听SW,绑定Listen
        self.butlisten.place(x=20, y=15)  # SW位置

        self.butclose = tkinter.Button(root, text="停止监听", command=self.Close)  # 创建停止监听SW,绑定Close
        self.butclose.place(x=120, y=15)

        self.edit = tkinter.Text(root)  # 创建文本框
        self.edit.place(y=50)  # 文本框位置

    def Listen(self):
        self.ctrl = Control(self.edit)  # 创建控制线程对象
        self.ctrl.setDaemon(True)  # 主线程结束后会把子线程结束
        self.ctrl.start()  # 启动线程

    def Close(self):
        print("over")
        self.ctrl.stop()  # 结束控制线程

root = tkinter.Tk()
window = Window(root)
root.mainloop()
