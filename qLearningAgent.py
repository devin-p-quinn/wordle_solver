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

    def __init__(self, alpha=1.0, epsilon=0.2, gamma=0.8, numTraining = 10):
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

    def setAlpha(self, alpha):
        self.alpha = alpha

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def getQValues(self):
        return self.qvalues

    def filterWords(self, state):
        """
        Filters list of potential actions (words) remaining after getting result of guess
        """
        j = 0
        guess = state[0]
        result = state[1]

        # Get letter counts
        for letter in result:
            if letter == 'g':
                self.green_letters[j] = guess[j]
            elif letter == 'b' and guess[j] not in self.black_letters:
                self.black_letters.append(guess[j])
            elif letter == 'y' and guess[j] not in self.yellow_letters:
                self.yellow_letters.append(guess[j])
            j += 1

        # Remove black letters from alphabet
        for letter in self.alphabet:
            if letter in self.black_letters:
                self.alphabet.remove(letter)

        for word in reversed(self.actions):
            for letter in range(len(word)):
                if word[letter] not in self.alphabet:  # Remove words containing black letters
                    self.actions.remove(word)
                    break
                if state[1][letter] == "g" and word[letter] != state[0][letter]:
                    self.actions.remove(word)
                    break


        if guess in self.actions:
            self.actions.remove(guess)
        return self.actions


    def getQValue(self, state, action):
        return self.qvalues[(state, action)]

    def getReward(self, state):
        """
        Reward function: rewards winning, getting green & yellow tiles
            and shrinking the list of potential actions by a greater amount
        """
        original_list_length = len(self.actions)
        # This will change the list of remaining words. Only call once state is determined
        self.filterWords(state)
        new_list_length = len(self.actions)
        reward = 0
        if wordle.checkWon(state[1]):
            reward += 1000
        else:
            for letter in state[1]:
                if letter == "g":
                    reward += 2
                if letter == "y":
                    reward += 1

            # Bonus for reducing the pool of potential next words
            if new_list_length != 0:
                reward += original_list_length / new_list_length

        return reward

    def computeValueFromQValues(self, state):
        """
        Find max q value of all possible actions from state
        """
        max_qval = -self.MAXINT
        for action in self.actions:
            temp = self.getQValue(state, action)
            if temp > max_qval:
                max_qval = temp

        return max_qval

    def computeActionFromQValues(self, state):
        """
        Compute the best action from list of remaining action based on Q value
        """
        best_action = None
        qval = -self.MAXINT

        """for action in self.actions:
            temp = self.getQValue(state, action)
            if temp > qval:
                qval = temp
                best_action = [action]
            if temp == qval:
                best_action == random.choice([best_action, action])
        return best_action"""

        value = self.computeValueFromQValues(state)
        actions = [action for action in self.actions
                   if self.getQValue(state, action) == value]
        return random.choice(actions)

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
        #print(self.qvalues)

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