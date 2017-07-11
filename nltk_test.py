import nltk

sentence = "It has been 150 years since the confederation of Canada!"

tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)

print(tagged)

from nltk.tag.stanford import StanfordNERTagger

st = StanfordNERTagger('../../nltk_data/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', '../../nltk_data/stanford-ner/stanford-ner.jar')
tokens = st.tag("Rami Eid is studying at Stony Brook University in NY".split())

print(tokens)