from ttkbootstrap import *

from openzip.utils.paths import CLIENT48_ICON_PATH, ONLINE16_ICON_PATH, OFFLINE16_ICON_PATH


class ClinetInfoFrame(Frame):
    def __init__(self, master, **kwargs):
        client_id = kwargs.pop("client_id", None)
        client_status = kwargs.pop("client_status", "online")

        super(ClinetInfoFrame, self).__init__(master=master)

        client_img = PhotoImage(file=CLIENT48_ICON_PATH)
        self.online_img = PhotoImage(file=ONLINE16_ICON_PATH)
        self.offline_img = PhotoImage(file=OFFLINE16_ICON_PATH)

        top_frame = Frame(self)

        client_logo_frame = Frame(top_frame)
        logo_label = Label(client_logo_frame, image=client_img)
        logo_label.image = client_img
        logo_label.pack(fill=BOTH)
        client_logo_frame.pack(side=LEFT, fill=Y, padx=5)

        client_info_frame = Frame(top_frame)

        clinet_id_frame = Frame(client_info_frame)
        Label(clinet_id_frame, text=f"Client id:", font=("", 10, "")).pack(side=LEFT)
        Label(clinet_id_frame, text=client_id, font=("", 10, "bold")).pack(side=LEFT)
        clinet_id_frame.pack(anchor=W)

        client_status_frame = Frame(client_info_frame)
        Label(client_status_frame, text=f"Client status:", font=("", 10, "")).pack(side=LEFT)
        self.status_label = Label(client_status_frame,
                                  text=client_status,
                                  font=("", 10, "bold"),
                                  image=self.online_img,
                                  compound=LEFT)
        self.status_label.image = self.online_img
        self.status_label.pack(side=LEFT)
        client_status_frame.pack(anchor=W)

        client_info_frame.pack(side=LEFT, fill=X)

        top_frame.pack(anchor=W, ipadx=1)

        Separator(self, style="primary").pack(fill=X, expand=True)

    def set_status(self, status: str):
        """
        :param status: 'online' or 'offline'
        """

        if status == "online":
            self.status_label.configure(image=self.online_img, text="online")
            self.status_label.image = self.online_img

        elif status == "offline":
            self.status_label.configure(image=self.offline_img, text="offline")
            self.status_label.image = self.offline_img
