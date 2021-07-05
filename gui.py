import tkinter as tk
import threading
from QueryGrade.query_grade import query_grade


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('成绩查询')
        self.master.geometry('500x365')
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()
        self.is_query = False

    def create_widgets(self):
        self.result = tk.Text(self)
        self.result.pack(side=tk.TOP)
        self.username_label = tk.Label(self, text="用户名")
        self.username_label.pack(side=tk.LEFT)
        self.username_input = tk.Entry(self)
        self.username_input.pack(side=tk.LEFT)
        self.password_label = tk.Label(self, text="密码")
        self.password_label.pack(side=tk.LEFT)
        self.password_input = tk.Entry(self, show="*")
        self.password_input.pack(side=tk.LEFT)
        self.query_button = tk.Button(
            self, text="查询", command=self.query, width=10)
        self.query_button.pack(side=tk.LEFT, padx=30, pady=10)

    def sub_thread(self, username, password):
        self.is_query = True
        res = query_grade(username, password, output=False)
        self.is_query = False
        self.result.delete("1.0", tk.END)
        self.result.insert("1.0", res)

    def query(self):
        self.result.delete("1.0", tk.END)
        if self.is_query:
            self.result.insert("1.0", "查询中，请勿重复查询...")
            return
        username = self.username_input.get().strip()
        password = self.password_input.get().strip()
        if len(username) == 0 or len(password) == 0:
            self.result.insert("1.0", "请输入用户名和密码...")
            return
        T = threading.Thread(target=self.sub_thread, args=(username, password))
        T.start()
        self.result.insert("1.0", "查询中...")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
