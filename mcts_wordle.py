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
    for letter in list(answer.values()):
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


    answerKey = {0:"b", 1:"b", 2:"b", 3:"b", 4:"b"}
    gLetters = []


    for i in range(len(theWord)):
        if theWord[i] == guess[i]:
            answerKey.update({i: "g"})
            gLetters.append(guess[i])
#            print(gLetters)
    for i in range(len(theWord)):
        if guess[i] in theWord and guess[i] not in gLetters:
            answerKey.update({i:"y"})
#        elif guess[i] not in theWord:
#            answerKey.update({i:"b"})

    return answerKey

def testMCTS():
    bestGuess = ["slate", "crane", "slant", "trace", "crate", "carte"]
    guess = random.choice(bestGuess)
    wordle = getWord()
    i = 0
    words = getWordList()
    good_words = []
    good_letters = []
#    green_letters = {0:"", 1:"", 2:"", 3:"", 4:""}
    green_letters = {}
    yellow_letters = []
    black_letters =[]
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
               'n','o','p','q','r','s','t','u','v','w','x','y','z']
    greenWords = []
    yellowWords = []
    wYellow = {}

    for i in range(6):
        wGreen = {}
        gGreen = []
        gYellow = []
#        guess = random.choice(bestGuess)
        answerKey = play(wordle, guess)
        print("Wordle: " + wordle + "\n")
        print("Current guess: " + guess + "\n")
        print(answerKey)


        if (checkWon(answerKey)):
            print("You won in " + str(i) + " attempts\n")
            print(wordle + " = " + guess)
            return i

        for i in range(len(answerKey)):
            if answerKey[i] == 'g':
                green_letters.update({i:guess[i]})
            elif answerKey[i] == 'y':
                yellow_letters.append(guess[i])
            elif answerKey[i] == 'b':
                if guess[i] in alphabet:
                    alphabet.remove(guess[i])
        print(green_letters)

        for word in reversed(words):
            for letter in word:
                if letter not in alphabet:
                    words.remove(word)
                    break
        print(f"Words length: {len(words)}")

        for word in words:
            for key, value in list(green_letters.items()):
                if word[key] != value:
                    words.remove(word)
                    break
        print(f"words length: {len(words)}")
        print(words)

        for word in words:
            weight = 0
            for key, value in list(green_letters.items()):
                if word[key] == value:
                    weight += 1
            wGreen.update({word:weight})

#        for word in list(wGreen.keys()):
        for word in words:
            weight = 0
            for letter in word:
                if letter in yellow_letters:
                    weight += 1
            wYellow.update({word:weight})


        wGreen = {key: val for key, val in sorted(wGreen.items(), key = lambda ele: ele[1], reverse = True)}
        wYellow = {key: val for key, val in sorted(wYellow.items(), key = lambda ele: ele[1], reverse = True)}

#        if len(words) > 0:
#            guess = random.choice(words)

        print(wYellow)
        for word, weight in wGreen.items():
            if weight == list(wGreen.values())[0]:
                gGreen.append(word)

        for word, weight in wYellow.items():
            if weight == list(wYellow.values())[0]:
                gYellow.append(word)

        print(wGreen)
        print("Grenn lenght:")
        print(len(wGreen))

        seed = random.randrange(1, 10)

        if seed < 2:
            if len(gYellow) > 0:
                guess = random.choice(gYellow)
        else:
            if len(gGreen) > 0:
                guess = random.choice(gGreen)

        print(gGreen)
        print(gYellow)
    return -1




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
    greenWords = []
    yellowWords = []
    wGreen = {}
    wYellow = {}
    gGreen = []

    while i < 6:
        answerKey = play(wordle, guess)
        print("Wordle: " + wordle + "\n")
        print("Current guess: " + guess + "\n")
        print(answerKey)


        if (checkWon(answerKey)):
            print("You won in " + str(i) + " attempts\n")
            print(wordle + " = " + guess)
            return i

        j = 0
        for letter in list(answerKey.values()):
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
                    if word in greenWords:
                        greenWords.remove(word)
                    if word in yellowWords:
                        yellowWords.remove(word)
                    break

        if guess in words:
            words.remove(guess)
        if guess in greenWords:
            greenWords.remove(guess)
        if guess in yellowWords:
            yellowWords.remove(guess)
        if guess in list(wGreen.values()):
            wGreen = {key:val for key, val in wGreen.items() if val != guess}

        if len(words) > 0:
            guess = random.choice(words)

        for word in words:
            if word[0] == green_letters[0] or word[1] == green_letters[1] or word[2] == green_letters[2] or word[3] == green_letters[3] or word[4] == green_letters[4] and word not in greenWords:
                greenWords.append(word)
                words.remove(word)

        for word in words:
            if word[0] in yellow_letters or word[1] in yellow_letters or word[2] in yellow_letters or word[3] in yellow_letters or word[4] in yellow_letters and word not in yellowWords:
                yellowWords.append(word)

        for word in yellowWords:
            if word in greenWords:
                yellowWords.remove(word)

        print("Green words: \n")
        print(greenWords)
        print("Yellow words: \n")
        print(yellowWords)
        if len(greenWords) > 0:
            guess = random.choice(greenWords)

        for word in greenWords:
            weight = 0
            for letter in word:
                if letter in green_letters.values():
                    weight += 1
                elif letter in yellow_letters:
                    weight += .25
                elif letter in black_letters:
                    weight += 0
            wGreen.update({word:weight})

        wGreen = {key: val for key, val in sorted(wGreen.items(), key = lambda ele: ele[1], reverse = True)}

        print("Weighted green: \n")
        print(wGreen)


        for word, weight in wGreen.items():
            if weight == list(wGreen.values())[0]:
                gGreen.append(word)

        if len(gGreen) > 0:
            guess = random.choice(gGreen)

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
    while i < 10000:
        sol = testMCTS()
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
#    print((play("crate", "blood")))
#    testMCTS()


if __name__ == "__main__":
    main()

