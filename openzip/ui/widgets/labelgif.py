import time

import _tkinter
from ttkbootstrap import *

from openzip.utils._threading import deamon_thread
from openzip.utils.paths import LOADING256_GIF_PATH


class LabelGif(Label):
    def __init__(self, *args, **kwargs):
        """
        A tkinter Label that supports the gif format, all args and kwargs that are used with
        a normal Label can be used also with the LabelGif.

        The only additional parameter is **gif** that rappresent the path of the gif image or an image object.
        """
        self._gif = kwargs.pop("gif", "")
        self._is_paused = False
        self._is_running = True
        super(LabelGif, self).__init__(*args, **kwargs)

        if self._gif:
            self.__gif_loop__()

    @deamon_thread
    def __gif_loop__(self):
        if isinstance(self._gif, Image.Image):
            img = self._gif

        else:
            img = Image.open(self._gif)

        frames_duration = []  # will contain the duration of each frames
        frames = []  # will contain the frames loaded with PhotoImage for tkinter

        img.seek(0)  # select the first frame
        while True:
            try:
                frames.append(ImageTk.PhotoImage(image=img.convert("RGBA"), format=f"gif -index {img.tell()}"))
                frames_duration.append(img.info['duration'] / 1000)  # duration is in milliseconds, convert in seconds

                # tell() returns the index of the current frame, add 1 for the next frame
                img.seek(img.tell() + 1)

            except EOFError:
                # raised when there are not more frames so seek() fail
                break

        while self._is_running:
            for duration, frame in zip(frames_duration, frames):
                while self._is_paused:
                    time.sleep(0.1)

                try:
                    self.configure(image=frame)
                    time.sleep(duration)

                except _tkinter.TclError:
                    # when destroy() is called on this object self.configure(image=frame) fail
                    break

    def pause(self, state: bool):
        """
        Stop the loop over the frames of the gif and keep showing the current frame if mode is True.

        :param state: True or False
        """
        self._is_paused = state

    def destroy(self) -> None:
        self._is_running = False  # to exit from the while loop
        super(Label, self).destroy()


if __name__ == "__main__":
    win = Window(themename="solar")
    lg = LabelGif(win, text="Loading..", gif=LOADING256_GIF_PATH, compound=TOP)
    lg.pack()
    Button(win, text="STOP", command=lambda: lg.pause(True)).pack(side=BOTTOM, pady=10)
    Button(win, text="START", command=lambda: lg.pause(False)).pack(side=BOTTOM, pady=10)
    win.withdraw()
    win.position_center()
    win.deiconify()
    win.mainloop()
