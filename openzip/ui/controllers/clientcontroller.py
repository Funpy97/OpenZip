import time
from tkinter import Widget

from ttkbootstrap import *

from openzip.networking.scanner import BaseScanner
from openzip.networking.zipclient import Client
from openzip.ui.views.clientview import ClientView
from openzip.ui.widgets.labelgif import LabelGif
from openzip.ui.widgets.serverinfoframe import ServerInfoFrame
from openzip.utils._threading import deamon_thread
from openzip.utils.paths import LOADING256_GIF_PATH


class ClientViewController:
    def __init__(self, view: ClientView):
        """
        Control the flow of events in the view ClientView.

        :param view: the view of the client
        """
        self.view = view

        self.view.btn_scann.configure(command=self.scann)

    @deamon_thread
    def scann(self):
        """
        When a new scanning is required by the user remove all the servers of the previous sanning
        and configure the scann button to disabled to prevent unnecessary multiple scanning.
        Show the LabelGif until the scanning process is completed and all the results (ServerInfoFrame) are
        inserted.
        Then configure the scann button back to normal.
        """
        self.clear_servers_frame()
        self.view.btn_scann.configure(state=DISABLED)

        lgif = LabelGif(self.view.rigth_frame,
                        text="Scanning your local network...",
                        gif=LOADING256_GIF_PATH,
                        font=("", 25, "bold"),
                        compound=TOP)
        lgif.pack(fill=Y, expand=True, anchor=CENTER)

        servers = BaseScanner().get_servers()

        for server in servers:
            sif = ServerInfoFrame(master=self.view.servers_found_frame,
                                  server_id=server.id,
                                  server_ip=server.ip,
                                  server_port=server.port)

            cmd = lambda frame=sif: self.start_client(frame)
            sif.btn_join.configure(command=cmd)
            sif.pack(anchor=W, fill=X)

        lgif.destroy()

        self.view.btn_scann.configure(state=NORMAL)

    @deamon_thread
    def start_client(self, frame: ServerInfoFrame):
        for child in self.view.rigth_frame.winfo_children():
            child.destroy()

        self.disable_left_frame()

        lgif = LabelGif(self.view.rigth_frame,
                        text="Connecting...",
                        gif=LOADING256_GIF_PATH,
                        font=("", 25, "bold"),
                        compound=TOP)
        lgif.pack(fill=Y, expand=True, anchor=CENTER)

        client = Client(frame.server_ip, nprocesses=self.view.cpus_number.get())
        client.start()

        # NOTE: .TButton for the style not only "success"
        frame.btn_join.configure(text="CONNECTED", style="success.TButton", command=None)

        lgif.configure(text=f"Connected with {frame.server_id}...")

        while client.is_running:
            time.sleep(0.1)

        lgif.destroy()

        label_completed = Label(self.view.rigth_frame, text="COMPLETED!", font=("", 30, "bold"))
        label_completed.pack(fill=Y, expand=True, anchor=CENTER)

        btn_completed = Button(self.view.rigth_frame, text="Finish", style="info.TButton")
        btn_completed.configure(command=lambda: [label_completed.destroy(),
                                                 btn_completed.destroy(),
                                                 self.enable_left_frame()])
        btn_completed.pack(side=BOTTOM, pady=10, padx=20, fill=X)

    def clear_servers_frame(self):
        for child in self.view.servers_found_frame.winfo_children():
            child.destroy()

    def disable_left_frame(self):
        """
        Disable the left spinbox and scann button, disable
        all the buttons in servers_found_frame where the text is "JOIN"
        """
        self.view.cpus_spinbox.configure(state=DISABLED)
        self.view.btn_scann.configure(state=DISABLED)

        def disable_join_buttons(container: Widget):
            for child in container.winfo_children():
                if isinstance(child, (Frame, LabelFrame)):
                    disable_join_buttons(container=child)

                elif isinstance(child, Button):
                    if child["text"] == "JOIN":
                        child.configure(state=DISABLED)

        disable_join_buttons(container=self.view.servers_found_frame)

    def enable_left_frame(self):
        self.view.cpus_spinbox.configure(state=NORMAL)
        self.view.btn_scann.configure(state=NORMAL)

        self.clear_servers_frame()
