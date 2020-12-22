"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao
-------------------------
File: breakoutgraphics.py
Name: Danny Tsai
-------------------------
This program provide breakout.py
some method to create a breakout game.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.graphics.gimage import GImage
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.gui.events.timer import pause
import random

BRICK_SPACING = 10     # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 50       # Height of a brick (in pixels).
BRICK_HEIGHT = 40      # Height of a brick (in pixels).
BRICK_ROWS = 5         # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 20      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 7.5      # Radius of the ball (in pixels).
PADDLE_WIDTH = 150     # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7.0  # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.

MONSTER_HP = 30        # Control hp increase per level og monster
HERO_ATTACK = 10       # Control attack of hero


class Monster:
    """
    This class can create monster present by brick.
    """
    def __init__(self, width, height, x=0, y=0, hp=MONSTER_HP):
        self.body = GRect(width, height, x=x, y=y)
        self.body.filled = True
        self.body.color = 'grey'
        self.l_eye = GOval(width*0.2, height*0.35, x=x+width*0.2, y=y+height*0.2)
        self.l_eye.filled = True
        self.r_eye = GOval(width*0.2, height*0.35, x=x+width*0.6, y=y+height*0.2)
        self.r_eye.filled = True
        self.hp = hp
        self.hp_label = GLabel(f'HP:{self.hp}')
        self.hp_label.x = self.body.x + (self.body.width - self.hp_label.width)/2
        self.hp_label.y = self.body.y + self.body.height


class Hero:
    """
    This class can create hero present by ball.
    """
    def __init__(self, width, height, x=0, y=0, attack=HERO_ATTACK):
        self.body = GOval(width, height, x=x, y=y)
        self.attack = attack


class BreakoutGraphics:
    """
    This class control the game rule and graphics drawing.
    """
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):
        # Instance Variable
        self.__game_status = False
        self.life_icon_list = []
        self.__monster_list = []
        self.__monster_dict = {}
        # Create a graphical window, with some extra space.
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 2.5 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)
        # Draw bricks as a monster.
        color = ['0xFFABAB', '0xFFE5B5', '0xFFFF45', '0xB5FFB5	', '0xC2C2FF']
        for row in range(brick_rows):
            for col in range(brick_cols):
                monster = Monster(brick_width, brick_height, x=col * (brick_width + brick_spacing),
                                  y=row * (brick_height + brick_spacing), hp=MONSTER_HP*(BRICK_ROWS-row))
                monster.body.fill_color = color[row]
                self.__monster_list.append(monster.body)
                self.__monster_dict[monster.body] = monster
                self.window.add(monster.body)
                self.window.add(monster.l_eye)
                self.window.add(monster.r_eye)
                self.window.add(monster.hp_label)
        # Create a paddle.
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.window.add(self.paddle, x=(self.window.width-self.paddle.width)/2,
                        y=self.window.height-paddle_offset)
        # Create score board
        self.score = 0
        self.score_label = GLabel(f'Score: {self.score}')
        self.score_label.font = '-20'
        self.window.add(self.score_label, x=0, y=self.window.height)
        # Center a filled ball in the graphical window as a hero.
        self.ball_radius = ball_radius
        self.hero = Hero(ball_radius * 2, ball_radius * 2)
        self.hero.body.filled = True
        self.hero.body.fill_color = 'black'
        self.set_hero_position()
        # Default initial velocity for the ball.
        self.__dx = 0
        self.__dy = 0
        # Initialize our mouse listeners.
        onmousemoved(self.set_paddle)
        onmouseclicked(self.game_start)

    def set_life_icon(self, life_number):
        """
        This method can set the life icon on graphic
        :param life_number: int, life number of initial
        """
        for i in range(life_number):
            life_icon = GImage('img/life.png')
            self.window.add(life_icon, x=self.window.width-(i+1)*life_icon.width,
                            y=self.window.height-life_icon.height)
            self.life_icon_list.append(life_icon)

    def remove_life_icon(self):
        """
        This method can remove the life icon on graphic
        """
        if len(self.life_icon_list) > 0:
            self.window.remove(self.life_icon_list[-1])
            self.life_icon_list.remove(self.life_icon_list[-1])

    def set_paddle(self, event):
        """
        This method control the paddle move with mouse.
        """
        if event.x <= self.paddle.width/2:
            self.paddle.x = 0
        elif event.x >= self.window.width - self.paddle.width/2:
            self.paddle.x = self.window.width - self.paddle.width
        else:
            self.paddle.x = event.x - self.paddle.width/2

    def game_start(self, event):
        """
        This method will start the game when mouse click.
        """
        if self.__game_status is False:
            self.__game_status = True
            self.__dx = random.randint(1, MAX_X_SPEED)
            if random.random() <= 0.5:
                self.__dx = -self.__dx
            self.__dy = INITIAL_Y_SPEED

    def set_hero_position(self):
        """
        This method will set ball at center of the window.
        """
        self.window.add(self.hero.body, x=(self.window.width-self.hero.body.width)/2,
                        y=(self.window.height-self.hero.body.height)/2)

    def next_life(self):
        """
        This method will reset ball position, game status and velocity for next life.
        """
        self.__game_status = False
        self.set_hero_position()
        self.__dx = 0
        self.__dy = 0

    def get_dx(self):
        """
        This method is a getter of dx.
        """
        return self.__dx

    def get_dy(self):
        """
        This method is a getter of dy.
        """
        return self.__dy

    def is_wall(self):
        """
        This method will identify the ball touch the wall,and change velocity.
        """
        if self.hero.body.x <= 0:
            self.__dx = abs(self.__dx)
        if self.hero.body.x >= self.window.width-self.hero.body.width:
            self.__dx = -abs(self.__dx)
        if self.hero.body.y <= 0:
            self.__dy = abs(self.__dy)

    def is_object(self):
        """
        This method will identify the ball touch the brick or paddle,
        if touch the paddle, the ball will change velocity,
        if touch the brick, the ball will remove it and change velocity.
        """
        check_point = [(self.hero.body.x, self.hero.body.y),
                       (self.hero.body.x + self.ball_radius*2, self.hero.body.y),
                       (self.hero.body.x, self.hero.body.y + self.ball_radius*2),
                       (self.hero.body.x + self.ball_radius*2, self.hero.body.y + self.ball_radius*2)]
        for i in range(len(check_point)):
            obj = self.window.get_object_at(check_point[i][0], check_point[i][1])
            if obj is not None:
                if obj == self.paddle:
                    self.__dy = -abs(self.__dy)
                elif obj in self.__monster_list:
                    self.attack_monster(obj)
                    if i == 0:  # left, top
                        self.__dy = abs(self.__dy)
                    elif i == 1:  # right, top
                        self.__dy = abs(self.__dy)
                    elif i == 2:  # left, bottom
                        self.__dy = -abs(self.__dy)
                    elif i == 4:  # right, bottom
                        self.__dy = -abs(self.__dy)
                break

    def attack_monster(self, obj):
        """
        This method will make hero attack monster.
        :param obj: GRect object, monster body touch by hero body.
        """
        damage = random.randint(1, 5) * self.hero.attack
        self.show_damage_number(damage)
        self.__monster_dict[obj].hp -= damage
        self.score += damage
        self.score_label.text = f'Score: {self.score}'
        if self.__monster_dict[obj].hp <= 0:  # monster dead after attack
            self.window.remove(obj)
            self.window.remove(self.__monster_dict[obj].l_eye)
            self.window.remove(self.__monster_dict[obj].r_eye)
            self.window.remove(self.__monster_dict[obj].hp_label)
            self.__monster_list.remove(obj)
        else:
            self.__monster_dict[obj].hp_label.text = f'HP:{self.__monster_dict[obj].hp}'

    def show_damage_number(self, damage):
        """
        This method can show damage number on the graphic
        :param damage: int, damage number
        """
        damage_label = GLabel(f'-{damage}')
        damage_label.color = 'red'
        damage_label.font = f'-{damage}'
        self.window.add(damage_label, x=self.hero.body.x + self.hero.body.width,
                        y=self.hero.body.y + self.hero.body.height)
        pause(80)
        self.window.remove(damage_label)

    def is_clear(self):
        """
        This method will identify is there exist brick or not.
        """
        if len(self.__monster_list) == 0:
            return True
        else:
            return False

    def set_end_massage(self, massage):
        """
        This method can show massage on center of graphic at the end of game.
        :param massage: str, massage want to show.
        """
        massage_label = GLabel(massage)
        massage_label.font = '-40'
        self.window.add(massage_label, x=(self.window.width - massage_label.width) / 2,
                        y=(self.window.height - massage_label.height) / 2)
