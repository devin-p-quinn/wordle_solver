'''
    CS5100
    Final Project
    Fall 2022
    Devin Quinn
    Annie Pates
'''

import qLearningAgent, wordle, naive_wordle

agent = qLearningAgent.QLearningAgent() # Initiate agent

def play(theWord, guess):
    '''
    Just like play function from wordle.py but makes key a string for easier hashing
    Function takes a guess word as the parameter and returns a list
    The list is a key to the wordle answer
    Each letter in the guess is shown next to a letter representing the key
    For Example:
        word: slate
        guess: slant
        ['g','g','g','b','y']
        'g' = green, letter in correct position
        'y' = yellow, letter in word not in correct position
        'b' = black, letter not in word'''

    #guess = ''.join(guess)

    answerKey = ""

    i = 0

    for wLetter in theWord:
        if wLetter == guess[i]:
            answerKey += ("g")
            i = i + 1
        elif guess[i] in theWord:
            answerKey += ("y")
            i = i + 1
        elif guess[i] not in theWord:
            answerKey += ("b")
            i = i + 1

    return answerKey

def runEpisode(numEpisode):
    "Set the wordle word"
    theWord = naive_wordle.getWord()
    initial_state = (None, "bbbbb")

    guess = agent.getAction(initial_state)  # Get first action based on initial state of all black

    i = 0
    while i < 6:
        state = (guess, play(theWord, guess))
        if numEpisode % 1000 == 0:
            print("Episode: ", numEpisode)
            print("Wordle: " + theWord)
            print("Current guess: " + guess + "\n")

        reward = agent.getReward(state)  # Calculate reward from guess

        # Win behavior
        if (wordle.checkWon(state[1])):
            if numEpisode % 1000 == 0:
                print("You won in " + str(i) + " attempts\n")
                print(theWord + " = " + guess)
            agent.reset()
            return i

        # Update qvalues
        next_guess = agent.getAction(state)
        next_state = (next_guess, play(theWord, next_guess))
        agent.update(state, next_guess, next_state, reward)

        guess = next_guess
        i += 1

    if numEpisode % 1000 ==0:
        print("No win\n")
        print("Wordle was: " + theWord + "\n")

    agent.reset()  # Reset word list etc in agent for new round
    return -1


def main():
    episodes = 1
    numEpisode = 0

    '''Main file for executing wordle program'''
    i = 0
    wins = 0
    attempts = 0
    losses = 0
    while i < episodes:
        sol = runEpisode(numEpisode)
        if sol > 0:
            wins += 1
            attempts += sol
        else:
            losses += 1
            attempts += 6
        i +=1
        numEpisode += 1

    print(agent.qvalues)

    print("Total wins: " + str(wins) + "\n")
    print("Total losses: " + str(losses) + "\n")
    print("Average attempts: " + str(attempts / episodes) + "\n")
    print("Win rate: " + str(wins / episodes) + "\n")


if __name__ == "__main__":
    main()

