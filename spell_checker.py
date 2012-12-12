import re
from get_letter_chosen import get_data_back

def word_count(path_for_file):
    f = open(path_for_file)
    read = f.read()
    f.close()
    lowercased = read.lower()
    cleaned_words = clean_words(lowercased)
    word_dict = {}

    for word in cleaned_words:
        word_dict[word] = word_dict.get(word, 0) + 1
    return word_dict

def clean_words(lowercased_text):
    cleaned_text = re.sub('[,._:;?!"{}1234567890()@\#$%^&*+=]-', ' ', lowercased_text)
    cleaned_text = cleaned_text.replace('--', ' ')

    cleaned_words = cleaned_text.split()
    return cleaned_words

# ENGLISH_DICTIONARY = word_count("seed_data/words.txt")

# def create_dictionary(dictionary):
#     g = open("seed_data/ENGLISH.txt", 'w')
#     for key, value in dictionary.iteritems():
#         row = "%s: \t%d \n" % (key, value)
#         print row
#         g.write(row)
#     g.close()

# do_it = create_dictionary(ENGLISH_DICTIONARY)

def read_dictionary():
    f = open("seed_data/ENGLISH.txt")
    lines = f.readlines()
    ENGLISH_DICTIONARY = {}
    for line in lines:
        word = line.split()
        ENGLISH_DICTIONARY[word[0]] = word[1]
    return ENGLISH_DICTIONARY
ENGLISH_DICTIONARY = read_dictionary()

def edit_distance1(word):
    nearest_letters = {'q' : 'wa', 'w' : 'esaq', 'e' : 'rdsw', 'r' : 'tfde', 't' : 'ygfr', 
                       'y' : 'uhgt', 'u' : 'ijhy', 'i' : 'okju', 'o': 'plki', 'p' : 'lo',
                       'a' : 'qwsz', 's' : 'wedxza', 'd' : 'erfcxs', 'f' : 'rtgvcd', 'g' : 'tyhbvf',
                       'h' : 'yujnbg', 'j' : 'uikmnh', 'k' : 'iolmj', 'l' : 'pko', 'z' : 'asx', 
                       'x' : 'sdcz', 'c' : 'dfvx', 'v' : 'fgbc', 'b' : 'ghnv', 'n' : 'hjmb', 'm' : 'jkn'}
    # not worrying about transpositions- 
    # I'm assuming people spell correctly, but are not perfect swipers
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    # if I accidentally included a letter they didn't mean to hit
    #### I should probably use the list of keys that are nearby instead of the whole alphabet for inserts.
    deletes = [a + b[1:] for a, b in splits if b]
    # if I missed a letter that should have been included
    inserts = [a + c + b for a, b in splits for c in alphabet]
    # if the swiper approached, but didn't hit, a letter they meant to,
    # or if they overshot a letter they meant to hit.
    # replaces = [a + c + b[1:] for a, b in splits for c in nearest_letters(b) if b]
    replaces = []
    for a, b in splits:
        if b:
            for c in nearest_letters[b[0]]:
                word = a + c + b[1:]
                replaces.append(word)
    return set(deletes + replaces + inserts)

# def get_english_dictionary():
#     f = open("seed_data/ENGLISH.txt")
#     read = f.read()
#     ENGLISH_DICTIONARY = eval(read)
#     return ENGLISH_DICTIONARY

def real_words_edit_dist2(word):
    return set(edit_dist_2 for edit_dist_1 in edit_distance1(word) for edit_dist_2 in edit_distance1(edit_dist_1) if ENGLISH_DICTIONARY.get(edit_dist_2))

def suggested_correction(word):
    if ENGLISH_DICTIONARY.get(word):
        return word
    else:
        edit_dist_1 = edit_distance1(word)
        potential_words = [word for word in edit_dist_1 if ENGLISH_DICTIONARY.get(word)]
        potential_words.extend(real_words_edit_dist2(word))
        best_guess = None
        selected_word = None
        for word in potential_words:
            value = ENGLISH_DICTIONARY[word]
            if value > best_guess:
                best_guess = value
                selected_word = word
        if selected_word == None:
            selected_word = 'Unknown'
        return selected_word
