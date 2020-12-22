"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao
-------------------------
File: breakoutgraphics.py
Name: Danny Tsai
-------------------------
This program use method of breakoutgraphics.py
create a breakout game.
"""

from campy.gui.events.timer import pause
from breakoutgraphics_ex import BreakoutGraphics

FRAME_RATE = 1000 / 120  # 120 frames per second.
NUM_LIVES = 3


def main():
    graphics = BreakoutGraphics()
    life = NUM_LIVES
    graphics.set_life_icon(life)
    # animation loop here!
    while True:
        graphics.hero.body.move(graphics.get_dx(), graphics.get_dy())
        if graphics.hero.body.y >= graphics.window.height:  # hero fallen down
            life -= 1
            graphics.remove_life_icon()
            if life > 0:  # still have life left
                graphics.next_life()
            else:
                graphics.set_end_massage('Game Over!')
                break
        elif graphics.is_clear() is True:  # break all the monster
            graphics.set_end_massage('You Win!')
            break
        else:
            graphics.is_wall()
            graphics.is_object()
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
