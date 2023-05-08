import os
import subprocess
from datetime import datetime
from time import sleep
import psutil


class BarItem:
    def __init__(
        self,
        filled: bool = False
    ) -> None:
        self.filled = bool(filled)
        self.out = ''

    def update(self) -> None:
        pass

    def __str__(self) -> str:
        return self.out

    def __bool__(self) -> bool:
        return self.filled


class Bar:
    def __init__(
        self,
        items_count: int = 10,
        sep: str = ''
    ) -> None:
        self.sep = sep
        self.items = [BarItem() for _ in range(items_count)]

    def start(self, wait: float = 0) -> None:
        """After call this function program will start infinity loop"""
        while True:
            for i in range(len(self.items)):
                self[i].update()
            self.write()
            sleep(wait)

    def __getitem__(
        self,
        key: int
    ) -> BarItem:
        return self.items[key]

    def __setitem__(
        self,
        key: int,
        value: BarItem
    ) -> None:
        self.items[key] = value

    def __len__(self) -> int:
        return len(self.items)

    def write(self, reversed: bool = True) -> None:
        out = ''.join(
            [str(self[i]) + ' | ' for i in range(len(self))
             if self[i]
             ]
        )[:-2]
        os.system(f"xsetroot -name \"{out}\"")


class TimeItem(BarItem):
    def __init__(self) -> None:
        super().__init__(True)

    def update(self) -> None:
        self.out = datetime.now().strftime("%H:%M:%S")


class RAMItem(BarItem):
    def __init__(self) -> None:
        """RAM in GiB"""
        super().__init__(True)
        self.divider = 2**30
        self.total = round(psutil.virtual_memory()[0] / self.divider, 1)

    def update(self) -> None:
        used = round(psutil.virtual_memory()[3] / self.divider, 1)
        self.out = f"RAM:{used}Gi/{self.total}Gi"


class LayoutItem(BarItem):
    def __init__(self) -> None:
        super().__init__(True)

    def update(self) -> None:
        self.out = str(subprocess.check_output(
            "setxkbmap -query | grep layout",
            shell=True
        ).split()[-1])[2:-1].upper()


def main() -> None:
    bar = Bar()
    bar[9] = TimeItem()
    bar[8] = RAMItem()
    bar[0] = LayoutItem()
    bar.start(1)


if __name__ == '__main__':
    main()
