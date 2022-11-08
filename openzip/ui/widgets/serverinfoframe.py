from ttkbootstrap import *

from openzip.utils.paths import SERVER48_ICON_PATH


class ServerInfoFrame(Frame):
    def __init__(self, master, server_id: str, server_ip: str, server_port: int, **kwargs):
        super(ServerInfoFrame, self).__init__(master=master, **kwargs)

        self.server_id = server_id
        self.server_ip = server_ip
        self.server_port = server_port

        server_img = PhotoImage(name="client48", file=SERVER48_ICON_PATH)

        top_frame = Frame(self)

        server_img_frame = Frame(top_frame)
        img_label = Label(server_img_frame, image=server_img)
        img_label.image = server_img
        img_label.pack(fill=BOTH, anchor=CENTER, expand=True)
        server_img_frame.pack(side=LEFT, fill=Y, padx=5)

        server_info_frame = Frame(top_frame)

        server_id_frame = Frame(server_info_frame)
        Label(server_id_frame, text=f"Server id:", font=("", 10, "")).pack(side=LEFT)
        Label(server_id_frame, text=server_id, font=("", 10, "bold")).pack(side=LEFT)
        server_id_frame.pack(anchor=W)

        # server_ip_frame = Frame(server_info_frame)
        # Label(server_ip_frame, text=f"Server ip:", font=("", 10, "italic")).pack(side=LEFT)
        # Label(server_ip_frame, text=server_ip, font=("", 10, "bold")).pack(side=LEFT, padx=5)
        # server_ip_frame.pack(anchor=W)
        #
        # server_port_frame = Frame(server_info_frame)
        # Label(server_port_frame, text=f"Server port:", font=("", 10, "italic")).pack(side=LEFT)
        # Label(server_port_frame, text=server_port, font=("", 10, "bold")).pack(side=LEFT, padx=5)
        # server_port_frame.pack(anchor=W)

        self.btn_join = Button(server_info_frame, text="JOIN", style="success-outline")
        self.btn_join.pack(anchor=W, fill=X)

        server_info_frame.pack(side=LEFT, fill=X)

        top_frame.pack(anchor=W)

        Separator(self, style="primary").pack(fill=X, pady=5, expand=True)
