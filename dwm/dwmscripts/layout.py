import json
import os
import sys


states = ["us", "ru"]


def main() -> None:
    state = states[1]
    if os.path.exists("/tmp/layout.json"):
        with open("/tmp/layout.json") as f:
            state = json.load(f)["layout"]
        for i, val in enumerate(states):
            if val == state:
                state = states[(i + 1) % len(states)]
                break
    with open("/tmp/layout.json", 'w') as f:
        json.dump({"layout": state}, f, indent=4)
    os.system(f"setxkbmap {state}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        if "-s" in sys.argv:
            os.system(f"setxkbmap {states[0]}")
