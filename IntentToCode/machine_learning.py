import collections
from collections import Counter
from tensorflow.keras.models import load_model
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re
import pickle
import numpy as np
from nltk import word_tokenize

training_model = load_model('cnn1.h5')
pkl_file = open('Departure_encoder1.pkl', 'rb')
encoder_model = pickle.load(pkl_file)
pkl_file.close()
pkl_file = open('dict_vectorizer1.pkl', 'rb')
dict_vectorizer = pickle.load(pkl_file)
pkl_file.close()

#Compare tags, checks old tags, if the tag determines it unclear, remove it.

def get_part_of_speech(word):
    probable_part_of_speech = wordnet.synsets(word)
    pos_counts = Counter()
    pos_counts["n"] = len([item for item in probable_part_of_speech if item.pos() == "n"])
    pos_counts["v"] = len([item for item in probable_part_of_speech if item.pos() == "v"])
    pos_counts["a"] = len([item for item in probable_part_of_speech if item.pos() == "a"])
    pos_counts["r"] = len([item for item in probable_part_of_speech if item.pos() == "r"])
    most_likely_part_of_speech = pos_counts.most_common(1)[0][0]
    return most_likely_part_of_speech

def clean_up_example(text):
    cleaned = re.sub('\W+', ' ', text)
    tokenized = word_tokenize(cleaned)
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(token, get_part_of_speech(token)) for token in tokenized]
    return lemmatized

#These properties could include informations about
# previous and next words as well as prefixes and suffixes.
def add_basic_features(sentence_terms, index):
    term = sentence_terms[index]
    return {
        'nb_terms': len(sentence_terms),
        'term': term,
        'is_first': index == 0,
        'is_last': index == len(sentence_terms) - 1,
        'is_capitalized': term[0].upper() == term[0],
        'is_all_caps': term.upper() == term,
        'is_all_lower': term.lower() == term,
        'prefix-1': term[0],
        'prefix-2': term[:2],
        'prefix-3': term[:3],
        'suffix-1': term[-1],
        'suffix-2': term[-2:],
        'suffix-3': term[-3:],
        'prev_word': '' if index == 0 else sentence_terms[index - 1],
        'next_word': '' if index == len(sentence_terms) - 1 else sentence_terms[index + 1]
    }

def give_tag(probabilities):
    #Take out index number of most probable in each list, then decodes them
    maximum = probabilities.max()
    index_of_maximum = np.where(probabilities == maximum)
    tag = encoder_model.inverse_transform(index_of_maximum[0])
    return tag


def call_for_machine_learning_POS(sentence):
    lem_list = []
    pos_tag_result =[]
    encoded_sentence = clean_up_example(sentence)

    for i in range(len(encoded_sentence)):
         lem_list.append(add_basic_features(encoded_sentence, i))
    pos_sentence = training_model.predict(dict_vectorizer.transform(lem_list))

    for i in range(len(lem_list)):
         tag = give_tag(pos_sentence[i])
         pos_tag_result.append([encoded_sentence[i], tag[0]])

    [pos_tag_result.remove(word) for word in pos_tag_result if 'DT' in word or 'CC' in word]
    return pos_tag_result