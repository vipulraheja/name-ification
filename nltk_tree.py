import os
import nltk
from nltk.tag.stanford import NERTagger

def traverse(t):
	print "in traverse"
	# try:
	# 	t.label()
	# except AttributeError:
	# 	print "in err"
	# 	print str(t) + " "
	# else:
		# Now we know that t.node is defined
	print('[', t.label()+ " ")
	for child in t:
		traverse(child)
	print(']'+ " ")

nouns = []
noun_nodes = []
verbs = []
verb_nodes = []
sbar_nodes = []

male_pronouns = ["he", "his"]
female_pronouns = ["she", "her"]

def inspectNoun(myTree, level):
	if myTree.node == "NP":
		nouns.append(level)
		noun_nodes.append(myTree.copy(True))
	if myTree.node == "VP":
		verbs.append(level)
		verb_nodes.append(myTree.copy(True))
	for child in myTree:
		if (type(child) is Tree):
			inspectNoun(child, level+1)

globvar = 0
globvar_nnp = 0
globvar_sbar = 0
globvar_verbpr = 0
globvar_comma = 0
globvar_FINAL = 0

def set_globvar(val):
    global globvar    # Needed to modify global copy of globvar
    globvar = val
    print_globvar()

def set_globvar_FINAL():
    global globvar_FINAL    # Needed to modify global copy of globvar
    globvar_FINAL = 1
    print_globvar_FINAL()

def set_globvar_nnp():
    global globvar_nnp    # Needed to modify global copy of globvar
    globvar_nnp = 1
    print_globvar_nnp()

def set_globvar_sbar():
    global globvar_sbar    # Needed to modify global copy of globvar
    globvar_sbar = 1
    print_globvar_sbar()

def set_globvar_verbpr(val):
    global globvar_verbpr    # Needed to modify global copy of globvar
    globvar_verbpr = val
    print_globvar_verbpr()

def print_globvar():
    print globvar     # No need for global declaration to read value of globvar

def print_globvar_nnp():
    print globvar_nnp     # No need for global declaration to read value of globvar

def print_globvar_sbar():
	print globvar_sbar

def print_globvar_FINAL():
	print globvar_FINAL

def print_globvar_verbpr():
	print globvar_verbpr

def inspectNounPR(myTree):
	if myTree.node == "PRP":
		print myTree.leaves()
		for leaf in myTree.leaves():
			print leaf.lower()
			if leaf.lower() in male_pronouns:
				set_globvar(1)
			elif leaf.lower() in female_pronouns:
				set_globvar(2)

	for child in myTree:
		if (type(child) is Tree):
			inspectNounPR(child)

def inspectNounNNP(myTree):
	if myTree.node == "NNP":
		set_globvar_nnp()

	for child in myTree:
		if (type(child) is Tree):
			inspectNounNNP(child)

def findSBAR(myTree):
	if myTree.node == "SBAR":
		print myTree.leaves()
		sbar_nodes.append(myTree.copy(True))
		set_globvar_sbar()

	for child in myTree:
		if (type(child) is Tree):
			findSBAR(child)	

def inspectVerbPR(myTree):
	if myTree.node == "PRP":
		print "FOUND PRP IN VERb treE"
		print myTree.leaves()
		for leaf in myTree.leaves():
			print leaf.lower()
			if leaf.lower() in male_pronouns:
				set_globvar_verbpr(1)
			elif leaf.lower() in female_pronouns:
				set_globvar_verbpr(2)

	for child in myTree:
		if (type(child) is Tree):
			inspectVerbPR(child)

def inspectVerbPRDollar(myTree):
	if myTree.node == "PRP$":
		print "FOUND PRP$ IN VERb treE"
		print myTree.leaves()
		for leaf in myTree.leaves():
			print leaf.lower()
			if leaf.lower() in male_pronouns:
				set_globvar_verbpr(1)
			elif leaf.lower() in female_pronouns:
				set_globvar_verbpr(2)

	for child in myTree:
		if (type(child) is Tree):
			inspectVerbPRDollar(child)

commas = []
def detectComma(myTree):
	print "detecting comma"
	if myTree.node == ",":
		print "COMMA FOUND"
		return True
	
	for child in myTree:
		if (type(child) is Tree): 
			if detectComma(child) is True:
				commas.append(myTree)

commatree = []
def inspectComma(myTree):
	found_comma = False
	print "-------------------------------"
	print myTree
	print "-------------------------------"
	for child in myTree:
		if found_comma is False and child.node == ",":
			found_comma = True
		if found_comma is True:
			commatree.append(child)

	print commatree
	for tr in commatree:
		# Case 1 after comma
		inspectNounPR(tr)
		if globvar != 0:
			if globvar == 1:
				print "MALE"
				set_globvar_FINAL()
				break
			if globvar == 2:
				print "FEMALE"
				set_globvar_FINAL()
				break

		# Case 2 after comma
		else:
			print "Checking for NP-->NNP ; VP-->SBAR-->PRP AFTER COMMA"
			set_globvar(0)
			inspectNounNNP(verb_nodes[0])
			print globvar_nnp
			print "Checking for NP-->NNP AFTER COMMA"
			if globvar_nnp == 1:
				if findSBAR(verb_nodes[0]) is True:
					inspectNounPR(sbar_nodes[0])
					if globvar_sbar != 0:
						if globvar == 1:
							print "MALE"
							set_globvar_FINAL()
							break
						if globvar == 2:
							print "FEMALE"
							set_globvar_FINAL()
							break
			
			else:
				print "Checking for VP-->SBAR-->PRP AFTER COMMA"
				inspectVerbPR(verb_nodes[0])
				print globvar_verbpr
				if globvar_verbpr != 0:
					if globvar_verbpr == 1:
						print "MALE"
						set_globvar_FINAL()
						break
					if globvar_verbpr == 2:
						print "FEMALE"
						set_globvar_FINAL()
						break


	if myTree.node == ",":
		print "FOUND COMMA IN TREE"
		print myTree.leaves()
		for leaf in myTree.leaves():
			print leaf.lower()
			if leaf.lower() in male_pronouns:
				set_globvar_verbpr(1)
			elif leaf.lower() in female_pronouns:
				set_globvar_verbpr(2)



def ExtractPhrases(myTree, phrase, level):
    myPhrases = []
    if (myTree.node == phrase):
        myPhrases.append( [level,myTree.copy(True)] )
    for child in myTree:
        if (type(child) is Tree):
            list_of_phrases = ExtractPhrases(child, phrase, level+1)
            if (len(list_of_phrases) > 0):
                myPhrases.extend(list_of_phrases)
    return myPhrases

def find_nearest_pronoun(text, NAME):
	sentence = text

	os.popen("echo \"" + sentence + "\" > ~/stanfordtemp.txt")

	parser_out = os.popen("~/stanford-parser-2012-11-12/lexparser.sh ~/stanfordtemp.txt").readlines()

	bracketed_parse = " ".join( [i.strip() for i in parser_out if len(i.strip()) > 0 and i.strip()[0] == "("] )
	print bracketed_parse

	st = bracketed_parse.replace("(. .)", "")
	tree2 =  nltk.tree.Tree(st)
	print tree2

	inspectNoun(tree2, 0)

	print noun_nodes
	print verb_nodes

	# Check case 1: NP-->PRP
	print "Checking for NP-->PRP"
	inspectNounPR(noun_nodes[0])
	if nouns[0] == verbs[0] and globvar != 0:
		if globvar == 1:
			print "MALE"
			set_globvar_FINAL()
		if globvar == 2:
			print "FEMALE"
			set_globvar_FINAL()

	# Check case 2: NP-->NNP ; VP-->SBAR-->PRP
	if globvar_nnp == 0 and globvar_FINAL == 0:
		print "Checking for NP-->NNP ; VP-->SBAR-->PRP"
		set_globvar(0)
		inspectNounNNP(verb_nodes[0])
		print globvar_nnp
		print "Checking for NP-->NNP"
		if globvar_nnp == 1:
			print "FOUND SBAR"
			if findSBAR(verb_nodes[0]) is True:
				inspectNounPR(sbar_nodes[0])
				if globvar_sbar != 0:
					if globvar == 1:
						print "MALE"
						set_globvar_FINAL()
					if globvar == 2:
						print "FEMALE"
						set_globvar_FINAL()
		
		else:
			print "Checking for VP-->SBAR-->PRP"
			inspectVerbPR(verb_nodes[0])
			print globvar_verbpr
			if globvar_verbpr != 0:
				if globvar_verbpr == 1:
					print "MALE"
					set_globvar_FINAL()
				if globvar_verbpr == 2:
					print "FEMALE"
					set_globvar_FINAL()

	if globvar_comma == 0 and globvar_FINAL == 0:
		set_globvar(0)
		set_globvar_verbpr(0)
		detectComma(tree2)

		if len(commas) > 0:
			inspectComma(commas[0])
		# else:
		# 	print verb_nodes[1]
		# 	inspectVerbPRDollar(verb_nodes[1])
		# 	print globvar_verbpr
		# 	if globvar_verbpr != 0:
		# 		if globvar_verbpr == 1:
		# 			print "MALE"
		# 		if globvar_verbpr == 2:
		# 			print "FEMALE"


	# print "\nNoun phrases:"
	# list_of_noun_phrases = ExtractPhrases(tree2, 'NP',0)
	# list_of_verb_phrases = ExtractPhrases(tree2, 'VP',0)
	# list_of_sbar_phrases = ExtractPhrases(tree2, 'SBAR',0)
	# for phrase in list_of_noun_phrases:
	# 	print " ", phrase
	# for phrase in list_of_verb_phrases:
	# 	print " ", phrase
	# for phrase in list_of_sbar_phrases:
	# 	print " ", phrase
	

# find_nearest_pronoun("Kim was scared that he would break her trust.")
# find_nearest_pronoun("Kim told Jaime to do his homework.", NAME)
# find_nearest_pronoun("Knowing that Mrs. Mallard was afflicted with a heart trouble, great care was taken to break to her as gently as possible the news of her husband's death")
# find_nearest_pronoun("It was Richards who had been in the newspaper office when intelligence of the railroad disaster was received, with Brently Mallard's name leading the list of killed.")
# find_nearest_pronoun("As Alejandro had studied a lot, he played football throughout the evening.")
# find_nearest_pronoun("Vish is going to her place")
# find_nearest_pronoun("Cinderella did the dishes, scrubbed the floor and made the bed all while her step-sisters rested on fancy beds had fun playing dress-up.")
# find_nearest_pronoun("Cinderella offered to help them get ready for the ball for she had excellent taste and despite how her step-sisters treated her, she always gave them the best advice")
# find_nearest_pronoun("Cinderella immediately went to get the finest pumpkin she could find.")