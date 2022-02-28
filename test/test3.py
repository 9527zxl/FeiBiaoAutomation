import os
import tkinter
import tkinter as tk
import tkinter.messagebox
from ttkbootstrap import Style

from tool.feibaio_tool import feibiao_login

window = tk.Tk()
window.title('飞镖自动化')
# 设置窗口大小及位置
window.geometry('300x300+500+200')

window.iconbitmap('../temporary/柠檬.ico')
window.resizable(width=False, height=False)
# 通过ttkbootstrap美化
style = Style()
Style(theme='minty')


# 主界面
def main():
    main = tk.Tk()
    main.title('欢迎您，今天的工作开始了')
    main.geometry('500x400+500+200')
    main.mainloop()


# 登录页面
def login():
    if account_input.get() == '':
        tkinter.messagebox.showinfo(title='error', message='账号不能为空!')
    elif password_input.get() == '':
        tkinter.messagebox.showinfo(title='error', message='密码不能为空!')

    username = account_input.get()
    password = password_input.get()
    # 登录飞镖网
    login_text = feibiao_login(username=username, password=password)
    tkinter.messagebox.showinfo(title='error', message=login_text)


def quit():
    # 终止程序
    os._exit(0)


login_text = tkinter.Label(window, text='登录飞镖网后台', font=('Arial', 19))
login_text.pack()

account_text = tkinter.Label(window, text='账号:', font=('Arial', 12), width=10, height=2)
account_text.place(x=10, y=80, width=80, height=20)
account_input = tkinter.Entry(window, width=20)
account_input.place(x=80, y=80, width=160, height=25)

password_text = tkinter.Label(window, text='密码:', font=('Arial', 12), width=10, height=2)
password_text.place(x=10, y=150, width=80, height=20)
password_input = tkinter.Entry(window, show='*', width=20)
password_input.place(x=80, y=150, width=160, height=25)

# 登录按钮
login = tkinter.Button(window, text="登录", font=('Arial', 10), command=login)
login.place(x=60, y=200, width=60, height=30)
# 退出按钮
quit = tkinter.Button(window, text="退出", font=('Arial', 10), command=quit)
quit.place(x=190, y=200, width=60, height=30)

window.mainloop()
