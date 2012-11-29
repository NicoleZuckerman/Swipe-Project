import re
from get_letter_chosen import get_data_back

def word_count(path_for_file):
    f = open(path_for_file)
    read = f.read()
    
    lowercased = read.lower()
    cleaned_words = clean_words(lowercased)
    word_dict = {}

    for word in cleaned_words:
        word_dict[word] = word_dict.get(word, 0) + 1
    f.close()
    # dict_file = open("seed_data/ENGLISH.txt", 'w')
    # for key in word_dict.keys():
    #     dict_entry = "%s \t %d \n" % (key, word_dict[key])
    #     write = dict_file.write(dict_entry)
    # dict_file.close()
    return word_dict

def clean_words(lowercased_text):
    # extraneous_characters = ',.-_:;?!"{}[]1234567890()@\#$%^&*+='
    cleaned_text = re.sub('[,.-_:;?!"{}1234567890()@\#$%^&*+=]', ' ', lowercased_text)
    # cleaned_text = lowercased_text.translate(' ', ',.-_:;?!"{}[]1234567890()@\#$%^&*+=')
    cleaned_text = cleaned_text.replace('--', ' ')
    cleaned_words = cleaned_text.split()
    return cleaned_words

ENGLISH_DICTIONARY = word_count("seed_data/words.txt")

# def dict_to_tuple_list():
#     key_value_list = []
    
#     for key, value in ENGLISH_DICTIONARY.iteritems():
#         paired_info = (key, value)
#         key_value_list.append(paired_info)
#     # print key_value_list
    
#     return key_value_list

# def order_by_occurance():
#     paired_list = dict_to_tuple_list()
#     occurance_word_list = []
    
#     for item in paired_list:
#         reversed_pair = (item[1], item[0])
#         occurance_word_list.append(reversed_pair)
    
#     low_to_high_ordered = occurance_word_list.sort()
#     high_to_low_ordered = occurance_word_list.reverse()
#     # print occurance_word_list
#     # f = open("seed_data/ENGLISH.txt", 'w')

#     for word in occurance_word_list:
#         print "%d: \t%s \n" % (word[0], word[1])
#     return occurance_word_list

# def keyboard_conversion():
#     keyboard = get_data_back('seed_data/user_keyboard.txt')
#     key_locations = []
#     for item in keyboard:
#         letter = item['letter']
#         x = item['x']
#         y = item['y']
#         # print "keyboard conversion-= letter %s, x %r, y %r" % (letter, x, y)
#         key_info = (letter, x, y)
#         key_locations.append(key_info)
#     # print "key locations: %r" % key_locations
#     return key_locations

# def nearest_letters(word_fragment):
#     keyboard = keyboard_conversion()
#     # print "keyboard: %r" % keyboard
#     chosen_letter = None
#     letter = word_fragment[0]
#     # print "letter is %s" % letter
#     for key in keyboard:
#         # print "key[0] is %s" % key[0]
#         if key[0] == letter:
#             chosen_letter = key
#             # print "chosen letter is %r" % chosen_letter[0]

#     possible_letters = []
#     for letter_item in keyboard:
#         letter_x = letter_item[1]
#         letter_y = letter_item[2]
#         letter = letter_item[0]
#         distance = pow((chosen_letter[1] - letter_x), 2) + pow((chosen_letter[2] - letter_y), 2)
#         distance_from_chosen = (distance, chosen_letter[0])
#         possible_letters.append(distance_from_chosen)
#     sorted_list = possible_letters.sort()
#     best_choices = possible_letters[1:7]
#     list_of_letter_options = []

#     for choice in best_choices:
#         list_of_letter_options.append(choice[1])
#     letters_within_one_key = " ".join(list_of_letter_options)
#     return letters_within_one_key

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
    # ENGLISH_DICTIONARY = get_english_dictionary()
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
        return selected_word
