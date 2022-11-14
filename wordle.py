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

    theWord = random.choice(words)

    guess = input("Enter guess: ")

    answerKey = {}

    for wLetter in theWord:
        if wLetter.equals()


if __name__ == "__main__":
    main()

