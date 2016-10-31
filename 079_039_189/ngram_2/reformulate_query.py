"""
Sanjay Reddy S-2013A7PS189P
Aditya Sarma  -2013A7PS079P
Vamsi T       -2013A7PS039P

Artificial Intelligence Term Project
"""


import nltk
import re

WEIGHT_FACTOR = 2.2
Q_WEIGHT_Quotes = 5
Q_WEIGHT_UnQuotes = 2


class Reformulated_Query():
    """
    This object has two variables the query (a string) and marks(an integer).
    When given a question, we reformulate into various combinations and for each one, we create the object.
    The marks variable is like a weight and denotes how probable the query string returns a relavant answer. 
    """

    def __init__(self, query, marks):
        self.query = query
        self.marks = marks
    def __str__(self):
    	print "Query is %s and Weight is %s" % (self.query, self.marks)
    	
    def __repr__(self):
    	return 	"Query is %s and Weight is %s" % (self.query, self.marks)


def reformulated_queries(question):
    """
    This function returns a list of Reformulated_Query objects by using various combinations of the given question (a string)
    """
    rewrites = [] 
    if('?' in question):
    	question = question[:-1]
    tokens = nltk.word_tokenize(question)
    verb = tokens[1] # assuming the second word is the main verb
    rewrites.append(Reformulated_Query("\"%s %s\"" % (verb, " ".join(tokens[2:])), Q_WEIGHT_Quotes))	
    i=2
    while(i<len(tokens)):
	temp="\"%s %s %s\"" % (" ".join(tokens[2:i+1]), verb, " ".join(tokens[i+1:]))
        reform=Reformulated_Query(temp,Q_WEIGHT_Quotes)
        rewrites.append(reform)
        i+=1
    
    reform = Reformulated_Query(" ".join(tokens[2:]), Q_WEIGHT_UnQuotes)           
    rewrites.append(reform)
    # print rewrites
    return rewrites
   
   

    

    
    
