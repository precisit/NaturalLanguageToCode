import nltk
import gensim
from nltk.corpus import treebank
from nltk.tokenize import word_tokenize
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec#model = Word2Vec.load(path/to/your/model)
import gensim.downloader as api
import pickle

#====INITIALIZE ========
def untagger(tagged_sentences):
    X = []
    for pos_tags in tagged_sentences:
                X.append(untag(pos_tags))
    return X

def untag(tagged_sentence):
    return [w for w, _ in tagged_sentence]

nltk.download('treebank')
sentences = treebank.tagged_sents(tagset='universal')
sentences = sentences[:len(sentences)]
input= untagger(sentences)

FILE = open("data.txt", "r")
listOFCommands = FILE.readlines()
FILE.close()
for command in listOFCommands:
    input.append(command.split())
print(input)
corpus = api.load('text8')
print(len(input))

path = get_tmpfile("word2vec.model")
model = gensim.models.Word2Vec(input, min_count=1)
model = Word2Vec(corpus)
model.train(sentences, total_examples=1, epochs=3)
model.save("word2vec.model")

model = Word2Vec.load('word2vec.model')
#print(model.wv.similarity('go', 'walk'))
print('hatchet:' , model.wv.similarity('axe', 'hatchet'))
print('run:' , model.wv.similarity('run', 'walk'))
print('run:' , model.wv.similarity('run', 'jump'))

model.most_similar('two')
print('Done')