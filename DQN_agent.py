import random
import numpy as np

from keras import Sequential
from collections import deque
from keras.layers import Dense
import matplotlib.pyplot as plt
from keras.optimizers import Adam

import argparse

# Env
from Paddle.paddle import Paddle
from Jump.jump import Jump
from Cannon.cannon import Cannon

from log_util import log_fn


parser = argparse.ArgumentParser()
parser.add_argument('--env', type=str, default='Paddle', help='Environments: [\'Paddle\', \'Jump\', \'Cannon\'].')
parser.add_argument('--num_episodes', type=int, default=100, help='The number of episodes to learn.')
parser.add_argument('--max_steps', type=int, default=1000, help='The maximum number of steps in each episode.')
parser.add_argument('--epsilon', type=float, default=1, help='The epsilon constant for epsilon-greedy policy.')
parser.add_argument('--epsilon_min', type=float, default=.01, help='The minimum value of epsilon with decay.')
parser.add_argument('--epsilon_decay', type=float, default=.995, help='The value for epsilon decay.')
parser.add_argument('--gamma', type=float, default=.95, help='The gamma constant for Q-value.')
parser.add_argument('--batch_size', type=int, default=64, help='The batch size.')
parser.add_argument('--learning_rate', type=float, default=0.001, help='The learning rate.')
parser.add_argument('--max_len', type=int, default=100000, help='The maximum length of experience replay memory.')

is_print = False


class DQN:

    """ Implementation of deep q learning algorithm """

    def __init__(self, action_space, state_space, args):
        self.action_space = action_space
        self.state_space = state_space
        self.epsilon = args.epsilon
        self.epsilon_min = args.epsilon_min
        self.epsilon_decay = args.epsilon_decay
        self.gamma = args.gamma
        self.batch_size = args.batch_size
        self.learning_rate = args.learning_rate
        self.memory = deque(maxlen=args.max_len)
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(64, input_shape=(self.state_space,), activation='relu'))  # Input is state space.
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_space, activation='linear'))  # Output is the predicted action from action space.

        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        # Apply epsilon-greedy policy
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        mini_batch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in mini_batch])
        actions = np.array([i[1] for i in mini_batch])
        rewards = np.array([i[2] for i in mini_batch])
        next_states = np.array([i[3] for i in mini_batch])
        dones = np.array([i[4] for i in mini_batch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma*(np.amax(self.model.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def train_dqn(episodes, env, args):
    loss = []

    action_space = env.get_action_space()
    state_space = env.get_state_space()
    max_steps = args.max_steps

    agent = DQN(action_space, state_space, args)
    for ep in range(episodes):
        state = env.reset()
        state = np.reshape(state, (1, state_space))
        score = 0
        for i in range(max_steps):
            action = agent.act(state)
            log_fn('action: {}'.format(action), is_print)
            reward, next_state, episode_done = env.step(action)
            score += reward
            next_state = np.reshape(next_state, (1, state_space))
            agent.remember(state, action, reward, next_state, episode_done)
            state = next_state
            agent.replay()
            if episode_done:
                print("episode: {}/{}, score: {}".format(ep, episodes, score))
                break
        loss.append(score)
    return loss


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
    loss = train_dqn(ep, env, args)
    plt.plot([i for i in range(ep)], loss)
    plt.xlabel('episodes')
    plt.ylabel('reward')
    plt.show()
