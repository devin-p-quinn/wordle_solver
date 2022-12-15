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
    """
    Runs an episode of the game (6 guesses)
    """
    # Set the wordle word
    theWord = naive_wordle.getWord()
    initial_state = (None, "bbbbb")
    print_interval = 1000

    guess = agent.getAction(initial_state)  # Get first action based on initial state of all black

    i = 1
    while i <= 6:
        state = (guess, play(theWord, guess))  # Make a guess
        if numEpisode % print_interval == 0:
            print("Episode: ", numEpisode)
            print("Wordle: " + theWord)
            print("Current guess: " + guess + "\n")

        reward = agent.getReward(state)  # Calculate reward from guess, also filters dictionary

        # Win behavior
        if (wordle.checkWon(state[1])):
            if numEpisode % print_interval == 0:
                print("You won in " + str(i) + " attempts")
                print(theWord + " = " + guess + "\n")
            agent.reset()
            return i

        # Update qvalues
        next_guess = agent.getAction(state)
        next_state = (next_guess, play(theWord, next_guess))
        agent.update(state, next_guess, next_state, reward)

        guess = next_guess
        i += 1

    # Print results
    if numEpisode % print_interval ==0:
        print("No win")
        print("Wordle was: " + theWord + "\n")

    agent.reset()  # Reset word list etc in agent for new round
    return -1


def main():
    """
    Run specified number of overall training episodes and track win % and average guesses needed
    """
    episodes = 10000
    numEpisode = 0

    i = 0
    wins = 0
    attempts = 0
    losses = 0
    while i < episodes:  # Run training
        sol = runEpisode(numEpisode)
        if sol > 0:
            wins += 1
            attempts += sol
        else:
            losses += 1
            attempts += 6
        i +=1
        numEpisode += 1

    #print(agent.qvalues)

    print("Total wins: " + str(wins))
    print("Total losses: " + str(losses))
    print("Average attempts: " + str(attempts / episodes))
    print("Win rate: " + str(wins / episodes) + "\n")

    """
    Run specified number of testing episodes based on trained QAgent. 
    Print overall win % and average number of guesses needed
    """
    testing_episodes = 1000
    num_testing_episode = 0

    agent.setAlpha(0)
    agent.setEpsilon(0)

    k = 0
    wins = 0
    attempts = 0
    losses = 0
    while k < testing_episodes:  # Run tests
        sol = runEpisode(num_testing_episode)
        if sol > 0:
            wins += 1
            attempts += sol
        else:
            losses += 1
            attempts += 6
        k +=1
        num_testing_episode += 1

    #print(agent.qvalues)

    print("Total testing wins: " + str(wins))
    print("Total testing losses: " + str(losses))
    print("Average testing attempts: " + str(attempts / testing_episodes))
    print("Testing win rate: " + str(wins / testing_episodes) + "\n")

if __name__ == "__main__":
    main()

