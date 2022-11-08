from openzip.ui.views.homeview import HomeView
from openzip.utils.constants import CLIENT_NAME, SERVER_NAME


# noinspection PyUnresolvedReferences
class HomeViewController:
    def __init__(self, view: HomeView):
        self.view = view

        self.view.server_btn.configure(command=lambda: self.view.master.set_view(SERVER_NAME))
        self.view.client_btn.configure(command=lambda: self.view.master.set_view(CLIENT_NAME))
