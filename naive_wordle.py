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
        else:
            answerKey.append("b")
            i = i + 1

    return answerKey

def testNaive():
    guess = "slate"
    word = getWord()
    i = 0
    words = getWordList()
    good_words = []
    good_letters = []
    green_letters = {}
    yellow_letters = []
    black_letters =[]
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
               'n','o','p','q','r','s','t','u','v','w','x','y','z']

    while i < 6:
        answerKey = play(word, guess)

        if (checkWon(answerKey)):
            print("You won in " + str(i) + " attempts\n")
            print(word + " = " + guess)
            return i

        j = 0
        for letter in answerKey:
            if letter == 'g':
                green_letters[j] = word[j]
            elif letter == 'b':
                black_letters.append(word[j])
            elif letter == 'y':
                yellow_letters.append(word[j])
            j += 1

#        print("Green letters: " + green_letters + "\n")
#        print("Black letters: " + black_letters + "\n")
#        print("Yellow letters: " + yellow_letters + "\n")

        for letter in alphabet:
            if letter in black_letters:
               alphabet.remove(letter)
#        print("Alphabet length: " + str(len(alphabet)) + "\n")

        for word in reversed(words):
            for letter in word:
                if letter not in alphabet:
                    words.remove(word)
                    break

        for word in list(words):
            for key in green_letters:
                if word[key] == green_letters[key]:
                    guess = word


#        print("Word list length: " + str(len(words)) + "\n")
        i += 1


    print("No win\n")
    print("Wordle was: " + word + "\n")

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
    while i < 10000:
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
    print("Average attempts: " + str(attempts / 10000) + "\n")
    print("Win rate: " + str(wins / 10000) + "\n")


if __name__ == "__main__":
    main()

