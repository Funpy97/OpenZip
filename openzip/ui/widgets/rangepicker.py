from ttkbootstrap import *


class SpinRangePicker(Frame):
    def __init__(self, master, **kwargs):
        minimum_value = kwargs.pop("min", 0)
        maximum_value = kwargs.pop("max", 99)
        labels_font = kwargs.pop("labels_font", "")
        labels_style = kwargs.pop("labels_style", "")
        final_text = kwargs.pop("final_label_text", "")

        super(SpinRangePicker, self).__init__(master, **kwargs)

        self.min_var = IntVar(self)
        self.min_var.set(minimum_value)
        self.max_var = IntVar(self)
        self.max_var.set(minimum_value)  # starts from the minimum valu

        f1 = Frame(self)
        Label(f1, text="From", style=labels_style, font=labels_font).pack(side=LEFT, padx=(0, 5))
        self.min_spinbox = Spinbox(f1,
                                   width=len(str(maximum_value)),
                                   from_=minimum_value,
                                   to=maximum_value,
                                   state=READONLY,
                                   command=self.__spinboxes_configure__,
                                   textvariable=self.min_var)
        self.min_spinbox.pack(side=LEFT)
        Label(f1, text="to", style=labels_style, font=labels_font).pack(side=LEFT, padx=5)
        self.max_spinbox = Spinbox(f1,
                                   width=len(str(maximum_value)),
                                   from_=minimum_value,
                                   to=maximum_value,
                                   state=READONLY,
                                   command=self.__spinboxes_configure__,
                                   textvariable=self.max_var)
        self.max_spinbox.pack(side=LEFT)
        Label(f1, text=final_text, style=labels_style, font=labels_font).pack(side=LEFT, padx=5)
        f1.pack()

    def __spinboxes_configure__(self):
        if self.min_var.get() > self.max_var.get():
            self.max_var.set(self.min_var.get())


if __name__ == "__main__":
    app = Window()
    SpinRangePicker(app).pack()
    app.mainloop()
