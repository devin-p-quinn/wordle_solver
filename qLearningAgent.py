'''
    CS5100
    Final Project
    Fall 2022
    Devin Quinn
    Annie Pates
'''
import random
from collections import defaultdict

import util
import wordle, naive_wordle


class QLearningAgent():
    """
    Implements Q-Learning approach to solving worldle.
    States are a tuple with the guess and the outcomes of guess (ex. ("slate", [gybbg])),
    and actions are the next word guessed
    """

    def __init__(self, alpha=1.0, epsilon=0.5, gamma=0.8, numTraining = 10):
        """
        Sets options, which can be passed in via the Pacman command line using -a alpha=0.5,...
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.discount = float(gamma)
        self.numTraining = int(numTraining)

        self.MAXINT = 999999999

        self.actions = naive_wordle.getWordList()
        self.green_letters = {0: "", 1: "", 2: "", 3: "", 4: ""}
        self.yellow_letters = []
        self.black_letters = []
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        # Initiate q-values
        self.qvalues = util.Counter()

    def filterWords(self, state):
        j = 0
        guess = state[0]
        result = state[1]
        for letter in result:
            if letter == 'g':
                self.green_letters[j] = guess[j]
            elif letter == 'b' and guess[j] not in self.black_letters:
                self.black_letters.append(guess[j])
            elif letter == 'y' and guess[j] not in self.yellow_letters:
                self.yellow_letters.append(guess[j])
            j += 1

        for letter in self.alphabet:
            if letter in self.black_letters:
                self.alphabet.remove(letter)

        for word in reversed(self.actions):
            for letter in word:
                if letter not in self.alphabet:
                    self.actions.remove(word)
                    break

        if guess in self.actions:
            self.actions.remove(guess)
        return self.actions


    def getQValue(self, state, action):
        return self.qvalues[(state, action)]

    def getReward(self, state):
        reward = 0
        if wordle.checkWon(state):
            reward += 1000
        else:
            for letter in state:
                if letter == "g":
                    reward += 2
                if letter == "y":
                    reward += 1
        return reward

    def computeValueFromQValues(self, state):
        max_qval = -self.MAXINT
        for action in self.actions:
            temp = self.getQValue(state, action)
            if temp > max_qval:
                max_qval = temp

        return max_qval

    def computeActionFromQValues(self, state):
        best_action = None
        qval = -self.MAXINT

        for action in self.actions:
            temp = self.getQValue(state, action)
            if temp > qval:
                qval = temp
                best_action = action
            if temp == qval:
                best_action == random.choice([best_action, action])

        return best_action

    def getAction(self, state):
        """
        Incorporates epsilon-greedy choice to achieve exploration/exploitation
        """
        if len(self.actions) == 0:
            return None
        best_action = self.computeActionFromQValues(state)

        r = random.random()
        if r < self.epsilon:
            return random.choice(self.actions)
        else:
            return best_action

    def update(self, state, action, nextState, reward):
        """
        Updates q-value table with new calculation of Q-value for current state, action
        """
        current_qval = self.getQValue(state, action)
        difference = reward + self.discount * self.computeValueFromQValues(nextState) - current_qval
        self.qvalues[state, action] = current_qval + self.alpha * difference

    def reset(self):
        """
        Resets actions to entire word list & result values to original states
        """
        self.actions = naive_wordle.getWordList()
        self.green_letters = {0: "", 1: "", 2: "", 3: "", 4: ""}
        self.yellow_letters = []
        self.black_letters = []
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        """def getQValue(self, state, action):
            features = self.getFeatures(state, action)
            dotProduct = 0

            for key in features:  # Compute dot product of featureVector and weightVector
                dotProduct += features[key] * self.weights[key]

        def update(self, state, action, nextState, reward: float):
            current_qval = self.getQvalue(state, action)
            difference = reward + self.discount * self.getValue(nextState) - current_qval

            features = self.getFeatures(state, action)
            for key in features:
                self.weights[key] = self.weights[key] + self.alpha * difference * features[key]

        def final(self, state):
            """