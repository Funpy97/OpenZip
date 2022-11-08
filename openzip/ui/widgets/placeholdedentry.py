from ttkbootstrap import *


class PlaceholdedEntry(Entry):
    def __init__(self, master, **kwargs):
        self._placeholder = kwargs.pop("placeholder", "")
        super(PlaceholdedEntry, self).__init__(master=master, **kwargs)

        self.insert(0, self._placeholder)

        self.bind("<FocusIn>", lambda x: self.on_focus_in())
        self.bind("<FocusOut>", lambda x: self.on_focus_out())

    def on_focus_in(self):
        if super(PlaceholdedEntry, self).get() == self._placeholder:
            self.delete(0, END)

    def on_focus_out(self):
        if not super(PlaceholdedEntry, self).get().strip():
            self.insert(0, self._placeholder)

    def get(self) -> str:
        return super(PlaceholdedEntry, self).get().replace(self._placeholder, "")


if __name__ == "__main__":
    app = Window()
    PlaceholdedEntry(app, placeholder="Some text...").pack(padx=30, pady=50)
    Button(app, text="SUBMIT").pack()
    app.mainloop()
