import traceback

from ttkbootstrap import *
from ttkbootstrap.dialogs.dialogs import Messagebox

from openzip.ui.controllers.clientcontroller import ClientViewController
from openzip.ui.controllers.homecontroller import HomeViewController
from openzip.ui.controllers.servercontroller import ServerViewController
from openzip.ui.views.clientview import ClientView
from openzip.ui.views.homeview import HomeView
from openzip.ui.views.serverview import ServerView
from openzip.utils.constants import (WIN_GEOMETRY,
                                     WIN_TITLE,
                                     HOME_NAME,
                                     SERVER_NAME,
                                     CLIENT_NAME,
                                     LIGTH_THEME_NAME,
                                     DARK_THEME_NAME)


class App(Window):
    def __init__(self):
        super(App, self).__init__(themename=LIGTH_THEME_NAME)

        self._style = Style()
        self.__init_styles__()

        # dark theme
        self.is_dark = BooleanVar(self)

        self.title(WIN_TITLE)
        self.geometry(WIN_GEOMETRY)

        self._current_view = None
        self._current_controller = None

        self._views = {HOME_NAME: {"view": HomeView, "controller": HomeViewController},
                       SERVER_NAME: {"view": ServerView, "controller": ServerViewController},
                       CLIENT_NAME: {"view": ClientView, "controller": ClientViewController}}

        Checkbutton(self, text="dark mode",
                    variable=self.is_dark,
                    command=self.set_theme_mode,
                    style="round-toggle").pack(side=TOP, anchor=W, padx=5, pady=5)

        self.set_view(name=HOME_NAME)

        self.iconify()
        self.withdraw()
        self.position_center()
        self.deiconify()

    def set_view(self, name: str):
        try:
            self._current_view.destroy()
            del self._current_controller

        except AttributeError:
            pass

        self.title(f"{self.title().split(' - ')[0]} - {name.upper()}")

        self._current_view = self._views[name]["view"](master=self)
        self._current_controller = self._views[name]["controller"](view=self._current_view)
        self._current_view.pack(fill=BOTH, expand=True)

    def set_theme_mode(self):
        if self.is_dark.get():
            self._style.theme_use(DARK_THEME_NAME)

        else:
            self._style.theme_use(LIGTH_THEME_NAME)

        self.__init_styles__()

    def __init_styles__(self):
        btn_layout_default = "TButton"
        btn_layout_home = "HomeView.TButton"
        frame_layout_borded = "Borded.TFrame"

        self._style.configure(btn_layout_home, font=("", 20, "bold"))
        self._style.configure(btn_layout_default, font=("", 10, "bold"))
        self._style.configure(frame_layout_borded, background="blue")

    def report_callback_exception(self, exc, val, tb):
        message = "".join(traceback.format_exception(exc, val, tb))
        Messagebox.show_error(parent=self, title="Error", message=message)


if __name__ == "__main__":
    app = App()
    app.mainloop()
