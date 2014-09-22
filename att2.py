import os
import nltk
from nltk.tag.stanford import NERTagger
from nltk import *

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

GENDER = ""

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

def set_globvar_FINAL(gender):
    global globvar_FINAL    # Needed to modify global copy of globvar
    global GENDER
    globvar_FINAL = 1
    print_globvar_FINAL()
    GENDER = gender

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

def inspectNounNNP(myTree, label):
	if myTree.node == "NNP":
		for leaf in myTree.leaves():
			print leaf
			if leaf == label:
				print "FOUND NAME!"
				set_globvar_nnp()

	for child in myTree:
		if (type(child) is Tree):
			inspectNounNNP(child, label)

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

verbpr_nodes = []
def inspectVerbNPR(myTree):
	print "detecting NP"
	if myTree.node == "NP":
		verbpr_nodes.append(myTree.copy(True))
		print "NP FOUND"
	
	for child in myTree:
		if (type(child) is Tree): 
			inspectVerbNPR(child)

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
def inspectComma(myTree, NAME):
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
				set_globvar_FINAL("male")
				break
			if globvar == 2:
				print "FEMALE"
				set_globvar_FINAL("female")
				break

		# Case 2 after comma
		else:
			print "Checking for NP-->NNP ; VP-->SBAR-->PRP AFTER COMMA"
			set_globvar(0)
			print "Checking for NP-->NNP"
			inspectNounNNP(noun_nodes[0], NAME)
			print globvar_nnp
			if globvar_nnp != 0:
				k = 1
				print "Finding SBAR"
				print verb_nodes[0]
				print "findsbar: " + str(findSBAR(verb_nodes[0]))
				findSBAR(verb_nodes[0])
				if len(sbar_nodes) > 0:
					print "Finding VP-->SBAR-->VP-->NP-->PRP"
					if len(verb_nodes) >= k:
						for verb_node in verb_nodes:
							print "HERE--- 1----"
							print verb_node
							inspectVerbNPR(verb_node)
							if len(verbpr_nodes) > 0:
								print "Digging into VP->NP"
								print verbpr_nodes[k]
								inspectNounPR(verbpr_nodes[k])
								inspectVerbPRDollar(verbpr_nodes[k])
								k = k + 1
								if globvar != 0 or globvar_verbpr != 0:
									if globvar == 1 or globvar_verbpr == 1:
										print "MALE"
										set_globvar_FINAL("male")
										break
									if globvar == 2 or globvar_verbpr == 2:
										print "FEMALE"
										set_globvar_FINAL("female")
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
			set_globvar_FINAL("male")
		if globvar == 2:
			print "FEMALE"
			set_globvar_FINAL("female")

	# Check case 2: NP-->NNP && VP-->SBAR-->PRP
	if globvar_nnp == 0 and globvar_FINAL == 0:
		print "Checking for NP-->NNP ; VP-->SBAR-->VP-->NP-->PRP"
		set_globvar(0)

		print "Checking for NP-->NNP"
		inspectNounNNP(noun_nodes[0], NAME)
		print globvar_nnp
		if globvar_nnp != 0:
			print "Finding SBAR"
			findSBAR(verb_nodes[0])
			if len(sbar_nodes) > 0:
				print "Finding VP-->NP-->PRP"
				inspectVerbNPR(sbar_nodes[0])
				if len(verbpr_nodes) > 0:
					inspectNounPR(verbpr_nodes[0])
					if globvar != 0:
						if globvar == 1:
							print "MALE"
							set_globvar_FINAL("male")
						if globvar == 2:
							print "FEMALE"
							set_globvar_FINAL("female")
			else:
				set_globvar_verbpr(0)
				k = 1
				if len(verbpr_nodes) >= 1:
					for verb_node in verb_nodes:
						print verb_node
						inspectVerbNPR(verb_node)
						if len(verbpr_nodes) > 0:
							print "Digging into VP->NP"
							print verbpr_nodes[k]
							inspectNounPR(verbpr_nodes[k])
							inspectVerbPRDollar(verbpr_nodes[k])
							k = k + 1
							if globvar != 0 or globvar_verbpr != 0:
								if globvar == 1 or globvar_verbpr == 1:
									print "MALE"
									set_globvar_FINAL("male")
									break
								if globvar == 2 or globvar_verbpr == 2:
									print "FEMALE"
									set_globvar_FINAL("female")
									break
		
	if globvar_comma == 0 and globvar_FINAL == 0:
		set_globvar(0)
		set_globvar_verbpr(0)
		detectComma(tree2)

		if len(commas) > 0:
			inspectComma(commas[0])

	return gender
	

# NAME = "Kim"
# find_nearest_pronoun("Kim was scared that he would break her trust.")
# find_nearest_pronoun("Kim told Jaime to do his homework.")
# find_nearest_pronoun("Knowing that Mrs. Mallard was afflicted with a heart trouble, great care was taken to break to her as gently as possible the news of her husband's death")
# find_nearest_pronoun("It was Richards who had been in the newspaper office when intelligence of the railroad disaster was received, with Brently Mallard's name leading the list of killed.")
# NAME = "Alejandro"
# find_nearest_pronoun("As Alejandro had studied a lot, he played football throughout the evening.")
# NAME = "Vish"
# find_nearest_pronoun("Vish is going to her place")
# NAME = "Cinderella"
# find_nearest_pronoun("Cinderella did the dishes, scrubbed the floor and made the bed all while her step-sisters rested on fancy beds had fun playing dress-up.")
# find_nearest_pronoun("Cinderella offered to help them get ready for the ball for she had excellent taste and despite how her step-sisters treated her, she always gave them the best advice")
# find_nearest_pronoun("Cinderella immediately went to get the finest pumpkin she could find.")

# print GENDER