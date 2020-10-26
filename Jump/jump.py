# Author: Vinod Kumar


import random
import turtle as t


class Jump:

    def __init__(self):
        self.kangaroo = 'assets/kangaroo.gif'
        self.screen_width = 900
        self.screen_length = 400
        self.episode_done = False
        self.hit, self.miss = 0, 0
        self.score_count = 0
        self.reward = 0
        self.triggered = False
        self.count = 20
        self.direction = 1
        self.speed = 5
        self.up_down_count = 20
        self.t_rex_speed = 5
        self.counter = 100

        # Obstacles
        self.set_obs()
        self.reset_obs()

        # Set up Background
        self.set_screen()

        # T rex - (kangaroo)
        self.set_t_rex()

        self.set_keyboard_control()

        self.set_score()

    def set_screen(self):
        self.win = t.Screen()
        self.win.addshape(self.kangaroo)
        self.win.title('Jump')
        self.win.bgcolor('black')
        self.win.setup(width=self.screen_width, height=self.screen_length)
        self.win.tracer(0)

    def set_obs(self):
        self.obs_size = 4
        self.obstacle_speed = -3
        self.start = -180
        self.end = -90
        self.diff = (self.end - self.start) / (self.obs_size - 1)

        self.color = ['orange', 'red', 'blue', 'green', 'yellow', 'cyan', 'purple', 'magenta']
        self.obs_height = [self.start + self.diff * i for i in range(self.obs_size)]
        self.obs = [t.Turtle() for _ in range((self.obs_size * 3) // 2)]

    def set_keyboard_control(self):
        self.win.listen()
        self.win.onkey(self.trigger_jump, 'space')

    def set_score(self):
        self.score = t.Turtle()
        self.score.speed(0)
        self.score.color('white')
        self.score.penup()
        self.score.hideturtle()
        self.score.goto(0, 160)
        self.score.write("Score : {}".format(self.score_count),
                         align='center',
                         font=('Courier', 24, 'normal'))

    def set_t_rex(self):
        self.t_rex = t.Turtle()
        self.t_rex.shape(self.kangaroo)  # Select a square shape

        self.t_rex.speed(0)
        self.t_rex.shapesize(stretch_wid=1.6, stretch_len=1.6)  # Streach the length of square by 5
        self.t_rex.penup()
        self.t_rex.color('white')  # Set the color to white
        self.t_rex.setx(-350)
        self.t_rex.sety(-175)

    def reset_obs(self):
        for i in self.obs:
            i.flag = False
            i.passed = False
            i.speed(0)
            i.shape('circle')  # Select a circle shape
            i.color(random.choice(self.color))
            i.penup()
            i.goto(self.screen_width / 2, 0)

    def reset_t_rex(self):
        self.triggered = False
        self.count = self.up_down_count
        self.direction = 1
        self.t_rex.goto(-350, -175)

    def trigger_jump(self):
        self.triggered = True

    def reset_score(self):
        self.score_count = 0
        self.update_score()

    def update_score(self):
        self.score.clear()
        self.score.write("Score : {}".format(self.score_count),
                         align='center',
                         font=('Courier', 24, 'normal'))

    def reset_ob(self, obs):
        obs.flag = False
        obs.passed = False
        obs.setx(self.screen_width / 2)

    def jump(self):
        if self.triggered:
            tex_y = self.t_rex.ycor()
            if self.count > 0:
                self.t_rex.sety(tex_y + self.direction * self.t_rex_speed)
                self.count -= 1
            elif self.count == 0 and self.direction == 1:
                self.count = self.up_down_count
                self.direction = -1
            elif self.count == 0 and self.direction == -1:
                self.triggered = False
                self.count = self.up_down_count
                self.direction = 1

    def move_previous_obstacles(self):
        for ob in self.obs:
            if ob.flag:
                if ob.xcor() + self.obstacle_speed < -1 * self.screen_width / 2:
                    self.reset_ob(ob)
                else:
                    if abs(self.t_rex.xcor() - ob.xcor()) <= 17 and abs(self.t_rex.ycor() - ob.ycor()) <= 25:
                        self.episode_done = True
                        self.reset()
                    elif not ob.passed and self.t_rex.xcor() > ob.xcor():
                        self.score_count += 1
                        ob.passed = True
                        ob.setx(ob.xcor() + self.obstacle_speed)
                        self.reward += 5
                        self.update_score()
                    else:
                        ob.setx(ob.xcor() + self.obstacle_speed)

    def run_frame(self):
        self.win.update()
        self.move_previous_obstacles()
        if self.counter % 60 == 0:
            r1 = random.randint(0, 4)
            if r1 != 0:
                for ob in self.obs:
                    if not ob.flag:
                        ob.flag = True
                        ob.sety(random.choice(self.obs_height))
                        break
                self.counter = 1
        else:
            self.counter += 1
        self.jump()

    # ------------------------ AI control ------------------------

    # 0 do nothing
    # 1 jump

    def reset(self):
        self.reset_obs()
        self.reset_t_rex()
        self.reset_score()
        state = [ob.xcor() * .01 for ob in self.obs] + [ob.ycor() * .01 for ob in self.obs] + [self.t_rex.ycor() * .01]
        return state

    def step(self, action):
        self.reward = 0
        self.episode_done = 0

        if action == 0:
            pass

        if action == 1:
            self.reward -= 1
            self.trigger_jump()

        self.run_frame()
        self.reward += .1

        # Reward at terminal state.
        if self.episode_done:
            self.reward -= 20

        state = [ob.xcor() * .01 for ob in self.obs] + [ob.ycor() * .01 for ob in self.obs] + [self.t_rex.ycor() * .01]
        return self.reward, state, self.episode_done


# ------- Human control ------- #
if __name__ == "__main__":
    env = Jump()

    while True:
        env.run_frame()