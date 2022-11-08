import multiprocessing
import zlib
from ctypes import c_bool, c_char, c_int64
from typing import Callable, Iterator

import more_itertools
import pyzipper

from openzip.utils.constants import MAX_PWD_LEN, MAX_CPU_PROCESSES


class OpenZipWithBruteforce:
    def __init__(self,
                 filepath: str,
                 pwd_generator: Iterator,
                 on_found_callback: Callable,
                 nprocesses: int = MAX_CPU_PROCESSES):
        # noinspection GrazieInspection
        """
        This class implement a brute force attack with parallelism
        by using the multiprocessing module.

        When an instance is created it will block the program until
        the password is found or the passwords to test are terminated.

        :param filepath: the path of the zip file
        :param pwd_generator: usually is an itertools.product() instance
        :param on_found_callback: when the password is found it call this Callable and pass the password as argument
        :param nprocesses: number of processes to run, should be less or equal to os.cpu_count()
        """

        self._filepath = filepath

        # Array object use a fixed size so this memory space will not be overwrited, can be shared between processes
        pwd = multiprocessing.Array(c_char, MAX_PWD_LEN)

        # Value object contain a value that can be shared and can be change by processes
        is_found = multiprocessing.Value(c_bool, False)
        self._is_running = multiprocessing.Value(c_bool, True)
        self._pwd_tested = multiprocessing.Value(c_int64, 0)

        processes = []

        for pwd_generator in more_itertools.distribute(nprocesses, pwd_generator):
            p = multiprocessing.Process(target=self.__bruteforce__,
                                        kwargs={"passwords": pwd_generator,
                                                "is_running": self._is_running,
                                                "is_found": is_found,
                                                "pwd": pwd,
                                                "pwd_tested": self._pwd_tested})
            processes.append(p)

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        for process in processes:
            process.terminate()
            process.kill()

        self._is_running.value = False

        # if i == 0 the value is empty (b"\x00"), pwd[:] returns integers that's why b"\x00" = 0
        str_pwd = "".join(chr(i) for i in pwd[:] if i != 0)

        if is_found.value:
            on_found_callback(str_pwd)

    def __bruteforce__(self, passwords: Iterator, is_running, is_found, pwd, pwd_tested):
        """
        NOTE: with a tiny archive, for example an archive that
        contains only a single empty txt file, this method could return
        a wrong password.
        """
        with pyzipper.AESZipFile(self._filepath, "r") as zf:
            for password in passwords:
                pwd_tested.value += 1
                if not is_running.value:
                    break

                password = "".join(password).encode()
                zf.setpassword(pwd=password)

                try:
                    zf.testzip()
                    pwd[:len(password)] = password
                    is_running.value = False
                    is_found.value = True
                    break

                except (RuntimeError, zlib.error):
                    continue

    @property
    def is_running(self) -> bool:
        return self._is_running.value

    @is_running.setter
    def is_running(self, flag: bool):
        self._is_running.value = flag

    @property
    def pwd_tested(self) -> int:
        return self._pwd_tested.value
