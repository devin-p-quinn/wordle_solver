'''
    CS5100
    Final Project
    Fall 2022
    Devin Quinn
    Annie Pates
'''
import random

def getWord():
    word_file = open("wordle_words.txt", "r")
    words = []
    for word in word_file:
        words.append(word_file.readline())

    word_file.close()
    theWord = random.choice(words)
    theWord = theWord.strip()
    return theWord

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
        else:
            answerKey.append("b")
            i = i + 1

    return answerKey


def main():
    '''Main file for executing wordle program'''
    word = getWord()
#    word = "slate"
    i = 0
    while i < 6:
        guess = input("Enter guess: ")
        answer = play(word, guess)
        print(answer)
        if checkWon(answer):
            print("Correct Word! You Win!: " + word)
            break
        i = i + 1


if __name__ == "__main__":
    main()

