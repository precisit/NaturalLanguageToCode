import nltk
from tensorflow import keras
import pickle
from nltk.corpus import treebank
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder

#================================================================================================#
#========================Proccesing the data for the models======================================#

nltk.download('treebank')
sentences = treebank.tagged_sents()
sentences = sentences[:len(sentences)//4]
tags = set([
    tag for sentence in treebank.tagged_sents()
    for _, tag in sentence
])
#print('nb_tags: %sntags: %s' % (len(tags), tags)) #number of tags we got

train_test_cutoff = int(.80 * len(sentences))
training_sentences = sentences[:train_test_cutoff]
testing_sentences = sentences[train_test_cutoff:]
train_val_cutoff = int(.25 * len(training_sentences))
validation_sentences = training_sentences[:train_val_cutoff]
training_sentences = training_sentences[train_val_cutoff:]


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


def untag(tagged_sentence):
    return [w for w, _ in tagged_sentence]


def transform_to_dataset(tagged_sentences):
    X, y = [], []
    for pos_tags in tagged_sentences:
            for index, (term, class_) in enumerate(pos_tags):
                # Add basic NLP features for each sentence term
                X.append(add_basic_features(untag(pos_tags), index))
                y.append(class_)
    return X, y

def untagger(tagged_sentences):
    X = []
    for pos_tags in tagged_sentences:
                X.append(untag(pos_tags))
    return X

X_train, y_train = transform_to_dataset(training_sentences)
X_test, y_test = transform_to_dataset(testing_sentences)
X_val, y_val = transform_to_dataset(validation_sentences)
simple_train_sentences = untagger(training_sentences)

#Our neural network takes vectors as inputs, so we need to convert our dict features to vectors.
# Fit our DictVectorizer with our set of features
dict_vectorizer = DictVectorizer(sparse=False)
dict_vectorizer.fit(X_train + X_test + X_val)
# Convert dict features to vectors
preX_train = training_sentences
X_train = dict_vectorizer.transform(X_train)
X_test = dict_vectorizer.transform(X_test)
X_val = dict_vectorizer.transform(X_val)

# Fit LabelEncoder with our list of classes
label_encoder = LabelEncoder()
label_encoder.fit(y_train + y_test + y_val)
output = open('Departure_encoder.pkl', 'wb')
pickle.dump(label_encoder, output)
output.close()

# Encode class values as integers
prey_train = y_train
y_train = label_encoder.transform(y_train)
y_test = label_encoder.transform(y_test)
y_val = label_encoder.transform(y_val)

# Convert integers to dummy variables (one hot encoded)
from keras.utils import np_utils
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
y_val = np_utils.to_categorical(y_val)

print("Done")
