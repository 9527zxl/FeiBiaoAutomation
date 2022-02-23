import tkinter as tk

from tool.patent_query_tool import login_patent_inquiry_gettoken

window = tk.Tk()
window.title('飞镖自动化')
window.geometry('500x700')

token = login_patent_inquiry_gettoken(2017107806169)
# 窗口的label
k = tk.Label(window,
             text=token,  # 文本
             bg='green',  # 字体的背景颜色
             font=('Arial', 12),  # 字体和大小
             width=30, height=2  # 字体所占的宽度和高度
             )
k.pack()  # 固定

window.mainloop()
