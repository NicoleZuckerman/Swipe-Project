def beefy_dict():
    words = {}
    f = open("seed_data/ENGLISH.txt", 'r+')

    lines = f.readlines()
    for line in lines:
        word = line.split()
        words[word[0]] = int(word[1])

    h = open("seed_data/count_1w.txt")
    norvig_lines = h.readlines()
    for norvig_line in norvig_lines:
        norvig_word = norvig_line.split()
        actual_word = norvig_word[0]
        word_occurance = int(norvig_word[1])
        if actual_word == 'view':
            print actual_word
            print word_occurance
        elif actual_word == 'pm':
            print actual_word
            print word_occurance

        words[actual_word] = words.get(actual_word, 0) + word_occurance
    h.close()

    for key in words.keys():
        dict_entry = "%s \t %d \n" % (key, words[key])
        write = f.write(dict_entry)
    f.close()
    return words

# (re-wrote the english dict to include not only my entries from project gutenberg books, but also peter norvig's words from the internet)
do_it = beefy_dict()


