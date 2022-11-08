import string
import time

from ttkbootstrap.constants import *

from openzip.networking.zipclient import Client
from openzip.networking.zipserver import ZipServer
from openzip.ui.views.serverview import ServerView
from openzip.ui.widgets.clientinfoframe import ClinetInfoFrame
from openzip.utils._threading import deamon_thread


class ServerViewController:
    def __init__(self, view: ServerView):
        self.view = view
        self.logger = view.logs_text
        self.server = None

        self.view.btn_start.configure(command=self.start)
        self.view.btn_stop.configure(command=self.stop)

    @deamon_thread
    def start(self):
        self.view.btn_start.configure(state=DISABLED)
        self.view.btn_stop.configure(state=NORMAL)

        self.logger.clear_log()
        self.clear_clients_frame()

        self.logger.add_log(message="Server initializing...",
                            level=self.logger.infolevel)

        try:
            self.server = ZipServer(filepath=self.view.zip_path.get(),
                                    charset=self.__get_charset__(),
                                    pwd_min_len=self.view.spin_range_picker.min_var.get(),
                                    pwd_max_len=self.view.spin_range_picker.max_var.get())
            self.server.start()

        except AssertionError as error:
            self.logger.add_log(message=error, level=self.logger.errorlevel)
            self.stop()
            return

        self.logger.add_log(message=f"Server (id: {self.server.server_id}) is running on "
                                    f"{self.server.server_ip}:{self.server.server_port}",
                            level=self.logger.infolevel)

        if self.view.join_on_start.get():
            this_client = Client(server_ip=self.server.server_ip,
                                 nprocesses=self.view.core_number.get(),
                                 client_id="You")
            this_client.start()

        clients = self.server.clients.copy()
        logged_clients_frame = {str: ClinetInfoFrame}

        while self.server.is_running:
            for client in self.server.clients:
                if client not in clients:
                    self.logger.add_log(message=f"New client connected {client.client_id} (addr: {client.client_addr})",
                                        level=self.logger.infolevel)
                    logged_clients_frame[client.client_id] = ClinetInfoFrame(master=self.view.clients_connected_frame,
                                                                             client_id=client.client_id,
                                                                             client_status="online")
                    logged_clients_frame[client.client_id].pack(anchor=W, fill=X)

                logged_clients_frame[client.client_id].set_status(status="online" if client.is_running else "offline")

            clients = self.server.clients.copy()
            time.sleep(0.2)

        if self.server.password_found:
            password = self.server.password_info.pwd
            client_id = self.server.password_info.client_id
            t = time.strftime("%H:%M:%S", self.server.password_info.localtime)

            self.logger.add_log(message=f"Password {password} found by {client_id} at {t}!",
                                level=self.logger.passwordlevel)

        self.stop()

    def stop(self):
        self.logger.add_log(message="Stopping the server...", level=self.logger.infolevel)

        self.view.btn_start.configure(state=NORMAL)
        self.view.btn_stop.configure(state=DISABLED)

        try:
            self.server.stop()
            self.logger.add_log(message="Server stopped!", level=self.logger.infolevel)

        except AttributeError:
            pass

    def clear_clients_frame(self):
        for frame in self.view.clients_connected_frame.winfo_children():
            frame.destroy()

    def __get_charset__(self):
        charset = []

        if self.view.ascii_uppercase.get():
            charset.extend(list(string.ascii_uppercase))

        if self.view.ascii_lowercase.get():
            charset.extend(list(string.ascii_lowercase))

        if self.view.ascii_digits.get():
            charset.extend(list(string.digits))

        if self.view.punctuation.get():
            charset.extend(list(string.punctuation))

        if self.view.additional_values.get():
            charset.extend(self.view.additional_values.get().split(","))

        charset = list(filter(None, set(charset)))

        assert charset, "Charset is empty."

        return charset
