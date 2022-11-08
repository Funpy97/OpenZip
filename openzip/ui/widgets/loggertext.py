import time

from ttkbootstrap.constants import END, DISABLED, NORMAL
from ttkbootstrap.scrolled import ScrolledText


class LoggerText(ScrolledText):
    infolevel = "inf"
    errorlevel = "err"
    passwordlevel = "pwd"

    def __init__(self, master, **kwargs):
        super(LoggerText, self).__init__(master=master, **kwargs)

        font = ("", 10, "bold")
        self.text.tag_configure(LoggerText.infolevel, foreground="blue", font=font)
        self.text.tag_configure(LoggerText.errorlevel, foreground="red", font=font)
        self.text.tag_configure(LoggerText.passwordlevel, foreground="green", font=font)

        self.text.configure(state=DISABLED)

    def add_log(self, message: str, level: str, time_format="%H:%M:%S"):
        self.text.configure(state=NORMAL)
        self.text.insert(END, f"[{time.strftime(time_format, time.localtime())}] {message}\n", level)
        self.text.see(END)
        self.text.configure(state=DISABLED)

    def clear_log(self):
        self.text.configure(state=NORMAL)
        self.text.delete(0.0, END)
        self.text.see(END)
        self.text.configure(state=DISABLED)
