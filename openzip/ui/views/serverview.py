import string
from tkinter.filedialog import askopenfilename

import ttkbootstrap.scrolled as scrolled
from ttkbootstrap import *

from openzip.ui.widgets.loggertext import LoggerText
from openzip.ui.widgets.placeholdedentry import PlaceholdedEntry
from openzip.ui.widgets.rangepicker import SpinRangePicker
from openzip.utils.constants import MAX_PWD_LEN, MAX_CPU_PROCESSES
from openzip.utils.paths import SERVER64_ICON_PATH, CLIENT64_ICON_PATH, LOG64_ICON_PATH


class ServerView(Frame):
    def __init__(self, master):
        super(ServerView, self).__init__(master=master)

        # charset
        self.ascii_uppercase = BooleanVar(self)
        self.ascii_lowercase = BooleanVar(self)
        self.ascii_digits = BooleanVar(self)
        self.punctuation = BooleanVar(self)

        # join on start
        self.join_on_start = BooleanVar(self)
        self.core_number = IntVar(self)
        self.core_number.set(1)

        top_frame = Frame(self)

        right = Frame(top_frame)
        server64_img = PhotoImage(name="server64", file=SERVER64_ICON_PATH)
        server_cfg_label_widget = Label(text="Server Configuration",
                                        font=("", 15, "bold"),
                                        image=server64_img,
                                        compound=RIGHT,
                                        style="secondary")
        server_cfg_label_widget.image = server64_img

        self.server_config_frame = LabelFrame(right, labelwidget=server_cfg_label_widget, labelanchor=NW)

        # file frame
        file_config_frame = Frame(self.server_config_frame)
        Label(file_config_frame, text="File", font=("", 12, "bold"), style="primary").pack(anchor=W)
        self.zip_path = PlaceholdedEntry(file_config_frame,
                                         placeholder="Select the file...",
                                         width=50)
        self.zip_path.pack(side=LEFT)
        Button(file_config_frame, text="Browse", command=self.configure_zip_file).pack(side=LEFT)
        file_config_frame.pack(anchor=W, padx=10, pady=10)

        # charset frame
        charset_config_frame = Frame(self.server_config_frame)
        Label(charset_config_frame, text="Charset", font=("", 12, "bold"), style="primary").pack(anchor=W)
        Checkbutton(charset_config_frame,
                    text=string.ascii_uppercase,
                    variable=self.ascii_uppercase).pack(anchor=W)
        Checkbutton(charset_config_frame,
                    text=string.ascii_lowercase,
                    variable=self.ascii_lowercase).pack(anchor=W)
        Checkbutton(charset_config_frame,
                    text=string.digits,
                    variable=self.ascii_digits).pack(anchor=W)
        Checkbutton(charset_config_frame,
                    text=string.punctuation,
                    variable=self.punctuation).pack(anchor=W)
        self.additional_values = PlaceholdedEntry(charset_config_frame,
                                                  width=50,
                                                  placeholder="Symbols or words separated with a comma...")
        self.additional_values.pack(anchor=W, pady=(3, 0))
        charset_config_frame.pack(anchor=W, padx=10, pady=10)

        # password frame
        password_config_frame = Frame(self.server_config_frame)
        Label(password_config_frame, text="Password length", font=("", 12, "bold"), style="primary").pack(anchor=W)
        self.spin_range_picker = SpinRangePicker(password_config_frame,
                                                 min=1,
                                                 max=MAX_PWD_LEN,
                                                 final_label_text="characters")
        self.spin_range_picker.pack()
        password_config_frame.pack(anchor=W, padx=10, pady=10)

        # join frame
        join_on_start_frame = Frame(self.server_config_frame)

        Label(join_on_start_frame, text="Join on start", font=("", 12, "bold"), style="primary").pack(anchor=W)
        Checkbutton(join_on_start_frame,
                    text="Join this device to the server on start",
                    variable=self.join_on_start,
                    command=self.cpus_cfg_frame_configuration).pack(anchor=W)

        cpus_cfg_frame = Frame(join_on_start_frame)
        Label(cpus_cfg_frame, text="Use").pack(side=LEFT)
        self.cores_spinbox = Spinbox(cpus_cfg_frame,
                                     from_=1,
                                     to=MAX_CPU_PROCESSES,
                                     width=2,
                                     textvariable=self.core_number,
                                     state=DISABLED)
        self.cores_spinbox.pack(side=LEFT, padx=5)
        Label(cpus_cfg_frame, text=f"core(s) of").pack(side=LEFT)
        Label(cpus_cfg_frame,
              text=f"{MAX_CPU_PROCESSES}",
              font=("", 11, "bold"),
              style="danger").pack(side=LEFT)
        Label(cpus_cfg_frame, text=f"to crack the file").pack(side=LEFT)
        cpus_cfg_frame.pack()

        join_on_start_frame.pack(anchor=W, padx=10, pady=10)
        self.server_config_frame.pack(anchor=W, pady=(15, 5), padx=5)

        self.btn_start = Button(right, text="START", style="success")
        self.btn_start.pack(fill=X, padx=5)
        self.btn_stop = Button(right, text="STOP", style="danger", state=DISABLED)
        self.btn_stop.pack(fill=X, pady=2, padx=5)
        right.pack(side=LEFT)

        left = Frame(top_frame)
        client64_img = PhotoImage(name="client64", file=CLIENT64_ICON_PATH)
        client_conn_label_widget = Label(text="Clients connected",
                                         font=("", 15, "bold"),
                                         image=client64_img,
                                         compound=RIGHT,
                                         style="secondary")
        client_conn_label_widget.image = client64_img

        clients_connected_labelframe = LabelFrame(left, labelwidget=client_conn_label_widget, labelanchor=NW)
        self.clients_connected_frame = scrolled.ScrolledFrame(clients_connected_labelframe,
                                                              autohide=True,
                                                              bootstyle="round")
        self.clients_connected_frame.pack(fill=BOTH, expand=True)
        clients_connected_labelframe.pack(pady=(15, 2), padx=5, fill=BOTH, expand=True)

        left.pack(side=LEFT, fill=BOTH, expand=True)

        top_frame.pack(side=TOP, fill=X)

        bottom_frame = Frame(self)
        log64_img = PhotoImage(name="log64", file=LOG64_ICON_PATH)
        server_log_label_widget = Label(text="Server logs",
                                        font=("", 15, "bold"),
                                        image=log64_img,
                                        compound=RIGHT,
                                        style="secondary")
        server_log_label_widget.image = log64_img

        self.server_log_frame = LabelFrame(bottom_frame, labelwidget=server_log_label_widget, labelanchor=NW)
        self.logs_text = LoggerText(self.server_log_frame, bootstyle="round")
        self.logs_text.pack(fill=BOTH, expand=True)
        self.server_log_frame.pack(pady=5, padx=5, fill=BOTH, expand=True)

        bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

    def configure_zip_file(self):
        filepath = askopenfilename(title="Select the encrypted zip file.",
                                   filetypes=[("Zip File", "*.zip")])

        if filepath:
            self.zip_path.delete(0, END)
            self.zip_path.insert(0, filepath)

    def cpus_cfg_frame_configuration(self):
        if self.join_on_start.get():
            self.cores_spinbox.configure(state=READONLY)

        else:
            self.cores_spinbox.configure(state=DISABLED)
