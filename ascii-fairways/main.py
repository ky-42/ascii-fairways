"""Golf game that is played in the terminal.

Tested on Pop!_OS 22.04 LTS
"""

import math
import os
import random
import time
from datetime import datetime, timedelta

FRAME_RATE_CAP = 45
FRAME_TIME = timedelta(seconds=1 / FRAME_RATE_CAP)


class Round:
    def __init__(self):
        term_size = os.get_terminal_size()

        self.grass_height = 4

        self.hole_pos = random.randint(term_size.columns // 4, term_size.columns - 7)
        self.hole_width = random.randint(3, 6)

        self.shot_angle = 45
        self.shot_power = 5

        self.shot = False
        self.ball_pos = [1, 0]
        self.ball_vel = [0, 0]

        self.shot_count = 0

        self.won = False

    def get_input(self) -> None:
        input_type = input(
            f"Shot count: {self.shot_count}, Current angle: {self.shot_angle}, Current power: {self.shot_power}\nPress enter to shoot or enter 'angle' or 'power' to adjust thier values: "
        )

        if input_type.lower().strip() == "angle":
            self.shot_angle = int(input("Enter a value between 0 and 90: "))
        elif input_type.lower().strip() == "power":
            self.shot_power = int(input("Enter a value between 1 and 10: "))
        elif input_type.strip() == "":
            self.ball_vel = [
                self.shot_power * math.cos((math.pi * self.shot_angle) / 180) * 15,
                self.shot_power * math.sin((math.pi * self.shot_angle) / 180) * 15,
            ]

            self.shot = True
            self.shot_count += 1

    def proccess_physics(self, delta) -> None:
        grav = -9.8 * 15
        self.ball_vel[1] = self.ball_vel[1] + (grav * delta)
        self.ball_pos[0] += self.ball_vel[0] * delta
        self.ball_pos[1] += self.ball_vel[1] * delta

        if self.ball_pos[1] < 0:
            self.shot = False

            if math.floor(self.ball_pos[0] % os.get_terminal_size().columns) in list(
                range(self.hole_pos, self.hole_pos + self.hole_width)
            ):
                self.won = True

    def render(self) -> str:
        render_str = ""

        terminal_size = os.get_terminal_size()

        render_str += (
            " " * math.floor(self.ball_pos[0] % terminal_size.columns)
            + "0"
            + "\n" * math.floor(self.ball_pos[1])
        )

        for i in range(self.grass_height):
            render_str += "\n"
            render_str += "#" * (self.hole_pos)
            render_str += " " * (self.hole_width)
            render_str += "#" * (
                terminal_size.columns - self.hole_pos - self.hole_width
            )
        render_str = (
            "\n" * (terminal_size.lines - render_str.count("\n") - 3) + render_str
        )

        return render_str


def main():
    current_round = Round()
    delta = 0

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        frame_start = datetime.now()

        print(current_round.render())
        if not current_round.shot:
            current_round.get_input()
        else:
            current_round.proccess_physics(delta)

            if current_round.won:
                current_round = Round()

        if frame_start + FRAME_TIME > (current_time := datetime.now()):
            delta = ((frame_start + FRAME_TIME) - current_time).total_seconds()
            time.sleep(delta)


if __name__ == "__main__":
    main()
