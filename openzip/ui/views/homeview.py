from ttkbootstrap import *

from openzip.utils.constants import WIN_GEOMETRY
from openzip.utils.paths import CLIENT256_ICON_PATH, SERVER256_ICON_PATH


class HomeView(Frame):
    def __init__(self, master):
        super(HomeView, self).__init__(master=master)

        server256_img = PhotoImage(name="server256", file=SERVER256_ICON_PATH)
        self.server_btn = Button(self,
                                 text="SERVER",
                                 image=server256_img,
                                 compound=BOTTOM,
                                 style="HomeView.TButton")
        self.server_btn.image = server256_img
        self.server_btn.pack(fill=BOTH, expand=True, pady=5, padx=10)

        client256_img = PhotoImage(name="client256", file=CLIENT256_ICON_PATH)
        self.client_btn = Button(self,
                                 text="CLIENT",
                                 image=client256_img,
                                 compound=BOTTOM,
                                 style="HomeView.TButton")
        self.client_btn.image = client256_img
        self.client_btn.pack(fill=BOTH, expand=True, pady=5, padx=10)


if __name__ == "__main__":
    app = Window()
    app.geometry(WIN_GEOMETRY)
    HomeView(app).pack(expand=True, fill=BOTH)
    app.mainloop()
