import itertools
import more_itertools
from typing import Union, List, Optional, Iterator


from openzip.utils.constants import MAX_PWD_LEN


class PasswordsManager:
    def __init__(self, charset: Union[List[str], str], pwd_min_len: int, pwd_max_len: int, split_in: int):
        assert pwd_min_len >= 0, "Password min length is 0"
        assert pwd_max_len <= MAX_PWD_LEN, f"Password max length is {MAX_PWD_LEN} chars"
        assert pwd_min_len <= pwd_max_len, "Password min length can't be higher than password max length"

        self._charset = charset
        self._pwd_min_len = pwd_min_len
        self._pwd_max_len = pwd_max_len

        split_in = split_in if self.passwords_amount > split_in else self.passwords_amount

        self._split_in = split_in

        self._generators = [itertools.product(charset, repeat=length)
                            for length in range(pwd_min_len, pwd_max_len + 1)]

        self._splitted_generators = [splitted_gen
                                     for generator in self._generators
                                     for splitted_gen in more_itertools.distribute(iterable=generator, n=split_in)]

        self._pwd_tested = 0

    def get_next_generator(self) -> Optional[Iterator]:
        if self._splitted_generators:
            return self._splitted_generators.pop()

    @property
    def passwords_amount(self) -> int:
        return sum(pow(len(self._charset), exp=length) for length in range(self._pwd_min_len, self._pwd_max_len + 1))

    @property
    def pwd_min_len(self) -> int:
        return self._pwd_min_len

    @property
    def pwd_max_len(self) -> int:
        return self._pwd_max_len

    @property
    def charset(self) -> Union[List[str], str]:
        return self._charset

    @property
    def pwd_tested(self):
        return self._pwd_tested

    @pwd_tested.setter
    def pwd_tested(self, value: int):
        self._pwd_tested = value

    @property
    def completed_percetage(self) -> float:
        """
        :return: a float value that rappresent the percentage of the completed task from 0.0 to 1.0
        """
        return round(self._pwd_tested / self.passwords_amount, 2)


if __name__ == "__main__":
    pm = PasswordsManager(charset="ABCD", pwd_min_len=2, pwd_max_len=3, split_in=2)
    amount = []

    while True:
        gen = pm.get_next_generator()
        if gen:
            for pwd in gen:
                print(pwd)
                amount.append(pwd)

        else:
            break

    print(f"Amount: {len(amount)}\nCalculated: {pm.passwords_amount}")

