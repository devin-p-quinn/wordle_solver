'''
    CS5100
    Final Project
    Fall 2022
    Devin Quinn
    Annie Pates
'''
import random

def getWord():
    words = getWordList()
    theWord = random.choice(words)

    return theWord

def getWordList():
    word_file = open("wordle_words.txt", "r")
    words = []
    for word in word_file:
        words.append(word_file.readline().strip())

    word_file.close()
    return words

def checkWon(answer):
    for letter in answer:
        if letter != 'g':
            return False
    return True

def play(theWord, guess):
    '''Function takes a guess word as the parameter and returns a list
    The list is a key to the wordle answer
    Each letter in the guess is shown next to a letter representing the key
    For Example:
        word: slate
        guess: slant
        ['g','g','g','b','y']
        'g' = green, letter in correct position
        'y' = yellow, letter in word not in correct position
        'b' = black, letter not in word'''

    guess = ''.join(guess)

    answerKey = []

    i = 0

    for wLetter in theWord:
        if wLetter == guess[i]:
            answerKey.append("g")
            i = i + 1
        elif guess[i] in theWord:
            answerKey.append("y")
            i = i + 1
        elif guess[i] not in theWord:
            answerKey.append("b")
            i = i + 1

    return answerKey

def testNaive():
    bestGuess = ["slate", "crane", "slant", "trace", "crate", "carte"]
    guess = random.choice(bestGuess)
    wordle = getWord()
    i = 0
    words = getWordList()
    good_words = []
    good_letters = []
    green_letters = {0:"", 1:"", 2:"", 3:"", 4:""}
    yellow_letters = []
    black_letters =[]
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
               'n','o','p','q','r','s','t','u','v','w','x','y','z']

    while i < 6:
        answerKey = play(wordle, guess)
        print("Wordle: " + wordle + "\n")
        print("Current guess: " + guess + "\n")


        if (checkWon(answerKey)):
            print("You won in " + str(i) + " attempts\n")
            print(wordle + " = " + guess)
            return i

        j = 0
        for letter in answerKey:
            if letter == 'g':
                green_letters[j] = guess[j]
            elif letter == 'b' and guess[j] not in black_letters:
                black_letters.append(guess[j])
            elif letter == 'y' and guess[j] not in yellow_letters:
                yellow_letters.append(guess[j])
            j += 1


        for letter in alphabet:
            if letter in black_letters:
               alphabet.remove(letter)

        for word in reversed(words):
            for letter in word:
                if letter not in alphabet:
                    words.remove(word)
                    break

        if guess in words:
            words.remove(guess)

        if len(words) > 0:
            guess = random.choice(words)

        for word in words:
#            for key in green_letters:
            if word[0] == green_letters[0] or word[1] == green_letters[1] or word[2] == green_letters[2] or word[3] == green_letters[3] or word[4] == green_letters[4]:
                guess = word
        i += 1


    print("No win\n")
    print("Wordle was: " + wordle + "\n")

    return -1


def main():
    '''Main file for executing wordle program'''
#    word = getWord()
#    word = "slate"
#    i = 0
#    while i < 6:
#        guess = input("Enter guess: ")
#        answer = play(word, guess)
#        print(answer)
#        if checkWon(answer):
#            print("Correct Word! You Win!: " + word)
#            break
#        i = i + 1
#    if not checkWon(answer):
#        print("you lose! Correct word: " + word)
    i = 0
    wins = 0
    attempts = 0
    losses = 0
    while i < 1000:
        sol = testNaive()
        if sol > 0:
            wins += 1
            attempts += sol
        else:
            losses += 1
            attempts += 6
        i +=1

    print("Total wins: " + str(wins) + "\n")
    print("Total losses: " + str(losses) + "\n")
    print("Average attempts: " + str(attempts / 1000) + "\n")
    print("Win rate: " + str(wins / 1000) + "\n")


if __name__ == "__main__":
    main()

