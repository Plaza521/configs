import os
import subprocess
from datetime import datetime
from time import sleep
import psutil


def get_command_out(command: str) -> None:
    return subprocess.check_output(
        command,
        shell=True
    ).decode("utf-8")


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
            ['[ ' + str(self[i]) + ' ] ' for i in range(len(self))
             if self[i]
             ]
        )[:-1]
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
        self.out = get_command_out(
            "setxkbmap -query | grep layout"
        ).split()[-1].upper()


class CPUUsageItem(BarItem):
    def __init__(self) -> None:
        super().__init__(True)

    def update(self) -> None:
        usage = psutil.cpu_percent()
        usage = f"{usage}" if usage % 1 else F"{int(usage)}.0"
        self.out = f"CPU:{usage:0>4}%"


class DiskUsageItem(BarItem):
    def __init__(self, divider: int = 10**9) -> None:
        super().__init__(True)
        """Disk in GB"""
        self.divider = 10**9
        self.total = round(psutil.disk_usage('/').total / self.divider, 1)

    def update(self) -> None:
        used = round(psutil.disk_usage('/').used / self.divider, 1)
        self.out = F"Disk:{used}G/{self.total}G"


class InfoItem(BarItem):
    def __init__(self, text: str) -> None:
        super().__init__(True)
        self.out = text


def main() -> None:
    kernel_ver = get_command_out("uname -r")[:-1]

    bar = Bar()
    bar[9] = TimeItem()
    bar[8] = RAMItem()
    bar[7] = DiskUsageItem()
    bar[6] = CPUUsageItem()

    bar[1] = InfoItem(kernel_ver)
    bar[0] = LayoutItem()
    bar.start(1)


if __name__ == '__main__':
    main()
