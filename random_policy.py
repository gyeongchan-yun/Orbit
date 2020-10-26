# this is a example code on how to use the environment.
# this code follow a random policy, means executes the random actions.


import numpy as np
import argparse

# import the env class
from Paddle.paddle import Paddle
from Jump.jump import Jump
from Cannon.cannon import Cannon


parser = argparse.ArgumentParser()
parser.add_argument('--env', type=str, default='Paddle', help='Environments: [\'Paddle\', \'Jump\', \'Cannon\'].')
parser.add_argument('--num_episodes', type=int, default=100, help='The number of episodes to learn.')
parser.add_argument('--max_steps', type=int, default=1000, help='The maximum number of steps in each episode.')


def random_policy(episodes, env, max_steps):
    action_space = env.get_action_space()
    state_space = env.get_state_space()
    max_steps = max_steps

    for ep in range(episodes):
        state = env.reset()
        score = 0

        for _ in range(max_steps):
            action = np.random.randint(action_space)
            reward, next_state, done = env.step(action)
            score += reward
            state = next_state
            if done:
                print("episode: {}/{}, score: {}".format(ep, episodes, score))
                break


if __name__ == '__main__':
    args = parser.parse_args()

    if args.env == 'Paddle':
        env = Paddle()
    elif args.env == 'Jump':
        env = Jump()
    elif args.env == 'Cannon':
        env = Cannon()
    else:
        raise ValueError('No such environment: {}'.format(args.env))

    np.random.seed(0)

    ep = args.num_episodes
    random_policy(ep, env, args.max_steps)
