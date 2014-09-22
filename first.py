import nltk
from nltk import word_tokenize

namelist = []

def gender_features(word):
	return {'suffix1': word[-1],
	'suffix2': word[-2:]}

def extract_entities(text):
	for sent in nltk.sent_tokenize(text):
		for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
			if hasattr(chunk, 'node'):
				if chunk.node == 'PERSON':
					print ' '.join(c[0] for c in chunk.leaves())
					namelist.append(' '.join(c[0] for c in chunk.leaves()))
					# print chunk.node, ' '.join(c[0] for c in chunk.leaves())

#text = """Some economists have responded positively to Bitcoin, including Francois R. Velde, senior economist of the Federal Reserve in Chicago who described it as "an elegant solution to the problem of creating a digital currency."""

text = """While  cleaning out  her husband's  attic, Mrs.  Phyllis Cahill inadvertently included among the items  sold to the pawnbroker a secreted  Ming  vase  John  Cahill had  stolen  from  the museum."""

#In November 2013 Richard Branson announced that 
#Virgin Galactic would accept Bitcoin as payment, saying that he had invested 
#in Bitcoin and found it "fascinating how a whole new global currency 
#has been created", encouraging others to also invest in Bitcoin.
#Other economists commenting on Bitcoin have been critical. 
#Economist Paul Krugman has suggested that the structure of the currency 
#incentivizes hoarding and that its value derives from the expectation that 
#others will accept it as payment. Economist Laura Summers has expressed 
#a "wait and see" attitude when it comes to Bitcoin. Nicolas, a market 
#strategist for ConvergEx Group, has remarked on the effect of increasing 
#use of Bitcoin and its restricted supply, noting, "When incremental 
#adoption meets relatively fixed supply, it should be no surprise that 
#prices go up. And that's exactly what is happening to BTC prices." """

extract_entities(text)

print namelist

from nltk.corpus import names
import random
names = ([(name, 'male') for name in names.words('male.txt')] +
		[(name, 'female') for name in names.words('female.txt')])
import random
random.shuffle(names)

featuresets = [(gender_features(n), g) for (n,g) in names]
train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)

for name in namelist:
	namestr = name
	print name + "," + str(classifier.classify(gender_features(namestr.split()[0])))

print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features(5)

train_names = names[1500:]
devtest_names = names[500:1500]
test_names = names[:500]

train_set = [(gender_features(n), g) for (n,g) in train_names]
devtest_set = [(gender_features(n), g) for (n,g) in devtest_names]
test_set = [(gender_features(n), g) for (n,g) in test_names]
classifier = nltk.NaiveBayesClassifier.train(train_set) 

print nltk.classify.accuracy(classifier, devtest_set) 

# errors = []
# for (name, tag) in devtest_names:
# 	guess = classifier.classify(gender_features(name))
# 	if guess != tag:
# 		errors.append( (tag, guess, name) )

# for (tag, guess, name) in sorted(errors): 
# 	print 'correct=%-8s guess=%-8s name=%-30s' % (tag, guess, name)

sample_set = [(gender_features(n)) for (n) in namelist]
for n in range(0,len(sample_set)):
	print namelist[n] + ": " + classifier.classify(sample_set[n])

# errors = []
# for (name, tag) in namelist:
# 	guess = classifier.classify(gender_features(name))
# 	if guess != tag:
# 		errors.append( (tag, guess, name) )

# for (tag, guess, name) in sorted(errors): 
# 	print 'correct=%-8s guess=%-8s name=%-30s' % (tag, guess, name)


text_t = word_tokenize(text)
tags = nltk.pos_tag(text_t)
for tag in tags:
    if tag[1] == "PRP":
        print tag[0]

