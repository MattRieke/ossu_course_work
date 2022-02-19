# Problem Set 2, hangman.py
# Name: Matt Rieke
# Collaborators:
# Time spent: 6 Hours

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    word_guess = False
    letter_match = False
    n = 0
    
    for schar in secret_word:
        n += 1
        for lchar in letters_guessed:
            if lchar == schar:
                letter_match = True
                break
        if letter_match == True and n == len(secret_word):
            word_guess = True
            break
        elif letter_match == True:
            letter_match = False
            continue
        else:
            break
    return word_guess


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word_guess = ''
    letter_match = False

    for schar in secret_word:
        for lchar in letters_guessed:
            if lchar == schar:
                letter_match = True
                break
        if letter_match == True:
            word_guess = word_guess + lchar
            letter_match = False
        else:
            word_guess = word_guess + '_ '
    return word_guess


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    all_letters = string.ascii_lowercase
    available_letters = []
    available_string = ''
    
    for all_char in all_letters:
        letter_available = True
        for val in letters_guessed:
            if val == all_char:
                letter_available = False
                break
        if letter_available == True:
            available_letters.append(all_char)
    for ava_char in available_letters:
        available_string = available_string + ava_char
    return available_string    
    

def letter_already_guessed(current_guess, letters_guessed):
    '''
    current_guess : String
        length of one, alpha only, current user guess
    letters_guessed : List
        list of strings, length one items, alpha only
    returns : boolean True if already guess or False if not already guessed
    '''
    for val in letters_guessed:
        if val == current_guess:
            return True
    return False


def is_in_word(current_guess, secret_word):
    '''
    current_guess : String
        length of one, alpha only, current user guess
    secret_word : String
        randomly selected word, alpha only, any length
    returns: boolean True if in word, boolean False if not in word
    '''
    for char in secret_word:
        if char == current_guess:
            return True
    return False

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print('\nWelcome to the game of Hangman!')
    #secret_word = choose_word(wordlist)
    #secret_word = 'hamburger'
    warning_count = 3
    guess_count = 6
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('\n------------\n')
    letters_guessed = []
    while guess_count > 0 and is_word_guessed(secret_word,letters_guessed) != True:
        print('You have', guess_count, 'guesses left.')
        print('Available letters:', get_available_letters(letters_guessed))
        current_guess = input('Please guess a letter: ')
        if current_guess.isalpha() == False:
            if warning_count > 0:
                warning_count -= 1
                print('Oops! That is not a valid letter. You have', warning_count, 'warnings left.')
                print('\n------------\n',)
                continue
            else:
                guess_count -= 1
                print('Oops! That is not a valid letter. You have', guess_count, 'guesses left.')
                print('\n------------\n',)
                continue
        else:
            current_guess = current_guess.lower()
            already_guessed = letter_already_guessed(current_guess, letters_guessed)
            if already_guessed == True:
                if warning_count > 0:
                    warning_count -= 1
                    print("Oops! You've already guessed that letter. You have", warning_count, 'warnings left.\n' + get_guessed_word(secret_word, letters_guessed))
                    print('\n------------\n',)
                    continue
                else:
                    guess_count -= 1
                    print("Oops! You've already guessed that letter. You have", guess_count, 'guesses left.\n' + get_guessed_word(secret_word, letters_guessed))
                    print('\n------------\n',)
                    continue
            else:
                letters_guessed.append(current_guess)
        in_word = is_in_word(current_guess, secret_word)
        if in_word == True:
            print('Good guess:', get_guessed_word(secret_word, letters_guessed))
            print('\n------------\n',)
            continue
        else:
            if current_guess in ['a','e','i','o','u']:
                guess_count -= 2
                print('Oops! That letter is not in my word:', get_guessed_word(secret_word, letters_guessed))
                print('\n------------\n',)
                continue
            else:
                guess_count -= 1
                print('Oops! That letter is not in my word:', get_guessed_word(secret_word, letters_guessed))
                print('\n------------\n',)
                continue
    if guess_count <= 0:
        print('Sorry you ran out of guesses. The word was', secret_word + '.')
    else:
        print('Congratulations, you won!')
        print('Your total score for this game is:', guess_count*len(secret_word))
        
    # FILL IN YOUR CODE HERE AND DELETE "pass"



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace(' ', '')
    match_word = True
    correct_guess = []
    if len(my_word) != len(other_word):
        match_word = False
        #print('not same length')
        return match_word
    for letter in my_word:
        if letter.isalpha() == True:
            if letter in correct_guess:
                continue
            else:
                correct_guess.append(letter)
    for item in correct_guess:
        for place in range(len(my_word)):
            if other_word[place] == item and my_word[place] != item:
                match_word = False
                #print('not my word')
                return match_word
            if other_word[place] != item and my_word[place] == item:
                match_word = False
                #print('not other word')
                return match_word
    return match_word
    # FILL IN YOUR CODE HERE AND DELETE "pass"



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    match_list = []
    match_string = ''
    for other_word in wordlist:
        if match_with_gaps(my_word, other_word) == True:
            match_list.append(other_word)
    if len(match_list) > 0:
        for item in match_list:
            match_string = match_string + ' ' + item
            match_string = match_string.lstrip()
        return match_string
    else:
        return 'No matches found'


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    print('\nWelcome to the game of Hangman!')
    #secret_word = choose_word(wordlist)
    #secret_word = 'hamburger'
    warning_count = 3
    guess_count = 6
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('\n------------\n')
    letters_guessed = []
    while guess_count > 0 and is_word_guessed(secret_word,letters_guessed) != True:
        print('You have', guess_count, 'guesses left.')
        print('Available letters:', get_available_letters(letters_guessed))
        current_guess = input('Please guess a letter: ')
        if current_guess == '*':
            print('Possible word matches are:')
            print(show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
            continue
        elif current_guess.isalpha() == False:
            if warning_count > 0:
                warning_count -= 1
                print('Oops! That is not a valid letter. You have', warning_count, 'warnings left.')
                print('\n------------\n',)
                continue
            else:
                guess_count -= 1
                print('Oops! That is not a valid letter. You have', guess_count, 'guesses left.')
                print('\n------------\n',)
                continue
        else:
            current_guess = current_guess.lower()
            already_guessed = letter_already_guessed(current_guess, letters_guessed)
            if already_guessed == True:
                if warning_count > 0:
                    warning_count -= 1
                    print("Oops! You've already guessed that letter. You have", warning_count, 'warnings left.\n' + get_guessed_word(secret_word, letters_guessed))
                    print('\n------------\n',)
                    continue
                else:
                    guess_count -= 1
                    print("Oops! You've already guessed that letter. You have", guess_count, 'guesses left.\n' + get_guessed_word(secret_word, letters_guessed))
                    print('\n------------\n',)
                    continue
            else:
                letters_guessed.append(current_guess)
        in_word = is_in_word(current_guess, secret_word)
        if in_word == True:
            print('Good guess:', get_guessed_word(secret_word, letters_guessed))
            print('\n------------\n',)
            continue
        else:
            if current_guess in ['a','e','i','o','u']:
                guess_count -= 2
                print('Oops! That letter is not in my word:', get_guessed_word(secret_word, letters_guessed))
                print('\n------------\n',)
                continue
            else:
                guess_count -= 1
                print('Oops! That letter is not in my word:', get_guessed_word(secret_word, letters_guessed))
                print('\n------------\n',)
                continue
    if guess_count <= 0:
        print('Sorry you ran out of guesses. The word was', secret_word + '.')
    else:
        print('Congratulations, you won!')
        print('Your total score for this game is:', guess_count*len(secret_word))



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
