from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledFrame

from openzip.utils.constants import MAX_CPU_PROCESSES
from openzip.utils.paths import CLIENT64_ICON_PATH


class ClientView(Frame):
    def __init__(self, master):
        super(ClientView, self).__init__(master=master)

        self.cpus_number = IntVar(self)
        self.cpus_number.set(1)

        left_frame = Frame(self)
        client64_img = PhotoImage(name="client64", file=CLIENT64_ICON_PATH)
        client_cfg_label_widget = Label(text="Client configuration",
                                        font=("", 15, "bold"),
                                        image=client64_img,
                                        compound=RIGHT,
                                        style="secondary")
        client_cfg_label_widget.image = client64_img

        self.client_cfg_frame = LabelFrame(left_frame, labelwidget=client_cfg_label_widget, labelanchor=NW)
        cpus_configuration_frame = Frame(self.client_cfg_frame)
        Label(cpus_configuration_frame, text="Core(s) to use", font=("", 12, "bold"), style="primary").pack(anchor=W,
                                                                                                            pady=5)
        Label(cpus_configuration_frame, text="Use").pack(side=LEFT)
        self.cpus_spinbox = Spinbox(cpus_configuration_frame,
                                    from_=1,
                                    to=MAX_CPU_PROCESSES,
                                    state=READONLY,
                                    width=2,
                                    textvariable=self.cpus_number)
        self.cpus_spinbox.pack(side=LEFT, padx=5)
        Label(cpus_configuration_frame, text=f" core(s) of").pack(side=LEFT)
        Label(cpus_configuration_frame,
              text=f"{MAX_CPU_PROCESSES}",
              font=("", 11, "bold"),
              style="danger").pack(side=LEFT)
        Label(cpus_configuration_frame, text=f"to crack the file").pack(side=LEFT)
        cpus_configuration_frame.pack(anchor=W, padx=10, pady=10)

        self.btn_scann = Button(self.client_cfg_frame, text="Search in my local network")
        self.btn_scann.pack(pady=20)

        self.servers_found_frame = ScrolledFrame(self.client_cfg_frame, autohide=True, bootstyle="round")
        self.servers_found_frame.pack(fill=BOTH, expand=True)

        self.client_cfg_frame.pack(pady=(15, 2), fill=Y, anchor=W, expand=True)

        left_frame.pack(side=LEFT, fill=Y)

        self.rigth_frame = Frame(self)
        self.rigth_frame.pack(side=LEFT, fill=BOTH, expand=True)
