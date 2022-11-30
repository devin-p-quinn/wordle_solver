'''
    CS5100
    Wordle
    Fall 2022
    Devin Quinn
'''
import random

def main():
    '''describe func here'''
    word_file = open("wordle_words.txt", "r")
    words = []
    for word in word_file:
        words.append(word_file.readline())

#    theWord = random.choice(words)
    theWord = "slate"

    guess = input("Enter guess: ")

    guess = ''.join(guess)

    answerKey = {}

    i = 0

    for wLetter in theWord:
        if wLetter == guess[i]:
            answerKey[guess[i]] = "g"
            i = i + 1
        elif guess[i] in theWord:
            answerKey[guess[i]] = "y"
            i = i + 1
        else:
            answerKey[guess[i]] = "b"
            i = i + 1

    print(answerKey)
    print(theWord)


if __name__ == "__main__":
    main()

