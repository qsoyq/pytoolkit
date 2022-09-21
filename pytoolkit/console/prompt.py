import sys
import termios
import tty

from typing import List, Optional

from rich.live import Live
from rich.text import Text


def new_text(selected: int, choices: List) -> Text:
    return Text("\n".join([f"{'>' if i == selected else ' '} {x}" for i, x in enumerate(choices)]))


def select_prompt(choices: List):
    selected = 0
    input_flag = 0

    def update(char: Optional[str]) -> Optional[Text]:
        nonlocal input_flag, selected

        if char is None:
            return new_text(selected, choices)

        if input_flag == 0 and char == '\x1b':
            input_flag = 1

        elif input_flag == 1 and char == '[':
            input_flag = 2

        elif input_flag == 2:
            char = '^' + char
            input_flag = 0

        if char == '\n':
            return None
        elif char == '^A':
            selected -= 1
        elif char == '^B':
            selected += 1

        selected = selected % len(choices)

        return new_text(selected, choices)

    settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    try:
        with Live(update(None), refresh_per_second=10) as live:
            while True:
                c = sys.stdin.read(1)
                text = update(c)

                if text is None:
                    return choices[selected]

                live.update(text)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
