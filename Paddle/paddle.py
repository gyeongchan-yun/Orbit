# Author: Shiva Verma


import turtle as t


class Paddle():

    def __init__(self):

        self.episode_done = False
        self.reward = 0
        self.hit, self.miss = 0, 0

        # Setup Background
        self.set_screen()
        # Paddle
        self.set_paddle()
        # Ball
        self.set_ball()
        # Score
        self.set_score()
        # Keyboard control
        self.set_keyboard_control()

    def set_screen(self):
        self.win = t.Screen()
        self.win.title('Paddle')
        self.win.bgcolor('black')
        self.win.setup(width=600, height=600)
        self.win.tracer(0)

    def set_paddle(self):
        self.paddle = t.Turtle()
        self.paddle.speed(0)
        self.paddle.shape('square')
        self.paddle.shapesize(stretch_wid=1, stretch_len=5)
        self.paddle.color('white')
        self.paddle.penup()
        self.paddle.goto(0, -275)

    def set_ball(self):
        self.ball = t.Turtle()
        self.ball.speed(0)
        self.ball.shape('circle')
        self.ball.color('red')
        self.ball.penup()
        self.ball.goto(0, 100)
        self.ball.dx = 3
        self.ball.dy = -3

    def set_score(self):
        self.score = t.Turtle()
        self.score.speed(0)
        self.score.color('white')
        self.score.penup()
        self.score.hideturtle()
        self.score.goto(0, 250)
        self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss),
                         align='center',
                         font=('Courier', 24, 'normal'),
                         )

    def set_keyboard_control(self):
        self.win.listen()
        self.win.onkey(self.paddle_right, 'Right')
        self.win.onkey(self.paddle_left, 'Left')

    # Paddle movement

    def paddle_right(self):
        x = self.paddle.xcor()
        if x < 225:
            self.paddle.setx(x+20)

    def paddle_left(self):
        x = self.paddle.xcor()
        if x > -225:
            self.paddle.setx(x-20)

    def run_frame(self):
        self.win.update()

        # Ball moving

        self.ball.setx(self.ball.xcor() + self.ball.dx)  # Update the ball's x-location using velocity
        self.ball.sety(self.ball.ycor() + self.ball.dy)  # Update the ball's y-location using velocity

        # Ball and Wall collision

        if self.ball.xcor() > 290:
            self.ball.setx(290)
            self.ball.dx *= -1

        if self.ball.xcor() < -290:
            self.ball.setx(-290)
            self.ball.dx *= -1

        if self.ball.ycor() > 290:
            self.ball.sety(290)
            self.ball.dy *= -1

        # Ball Ground contact

        if self.ball.ycor() < -290:
            self.ball.goto(0, 100)
            self.miss += 1
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss),
                             align='center',
                             font=('Courier', 24, 'normal'),
                             )
            self.reward -= 3
            self.episode_done = True

        # Ball Paddle collision

        if abs(self.ball.ycor() + 250) < 2 and abs(self.paddle.xcor() - self.ball.xcor()) < 55:
            self.ball.dy *= -1
            self.hit += 1
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss),
                             align='center',
                             font=('Courier', 24, 'normal'),
                             )
            self.reward += 3

    # ------------------------ AI control ------------------------

    """
    Action space
    - 0: Move left
    - 1: Do nothing
    - 2: Move right
    """

    """
    State space
    - Position of the paddle in the x-axis.
    - Position of the ball in the x, y-axis.
    - The velocity of the ball in the x, y-axis.
    """

    def get_action_space(self):
        return 3

    def get_state_space(self):
        return 5

    def reset(self):
        self.paddle.goto(0, -275)
        self.ball.goto(0, 100)
        state = [self.paddle.xcor()*0.01,
                 self.ball.xcor()*0.01, self.ball.ycor()*0.01,
                 self.ball.dx, self.ball.dy
                 ]
        return state

    def step(self, action):
        self.reward = 0
        self.episode_done = False

        if action == 0:
            self.paddle_left()
            self.reward -= .1

        if action == 1:
            pass

        if action == 2:
            self.paddle_right()
            self.reward -= .1

        self.run_frame()

        state = [self.paddle.xcor()*0.01,
                 self.ball.xcor()*0.01, self.ball.ycor()*0.01,
                 self.ball.dx, self.ball.dy
                 ]
        return self.reward, state, self.episode_done


# ------- Human control ------- #
if __name__ == "__main__":
    env = Paddle()

    while True:
        env.run_frame()

