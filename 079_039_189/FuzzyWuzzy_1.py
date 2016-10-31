"""
Sanjay Reddy S-2013A7PS189P
Aditya Sarma  -2013A7PS079P
Vamsi T       -2013A7PS039P

Artificial Intelligence Term Project
"""

import nltk
from fuzzywuzzy import fuzz,process

words=["the","of","is","has","in","many"] #these are common words which have to be removed from strings


data_who=[("discovered radio carbon dating","Williard F. Libby"),
	  ("directed gone with wind","Victor Fleming, Cukor and Sam Wood"),
	  ("composed opera semiramide","Gioacchino Rossi"),
	  ("wrote gift magi","Henry O."),
	  ("fifth president united states","James Monroe")]

data_what=[("south american country largest population","Brazil"),
	   ("largest city florida","Jacksonville"),
	   ("planet smallest surface area","Pluto")]

data_how=[("people live in israel","8,049,314"),
          ("far mount kilimanjaro from mount everest","3,892 miles"),
          ("far neptune from sun","2,798,800,000 miles")]
        

def enter(MSG):
    """
    This function takes a string (MSG) and tries to answer the query by looking through the dictionaries in the program (after some preprocessing).
    It tries to mine out the correct response by performing pattern matching through the structured data
    """
    msg=MSG.lower()
    if msg[-1]=='?':
        msg=msg[:-1]
    tokens=nltk.word_tokenize(msg)
    for i in words:
        while (i in tokens):
            tokens.remove(i)
    lst=[]
    flag=0
    if tokens[0]=="who":
        lst=data_who
    elif tokens[0]=="what":
        lst=data_what
    elif tokens[0]=='how':
        lst=data_how
    #msg=str(tokens)
    msg=' '.join(tokens[1:])    
    for i in lst:
        if fuzz.token_set_ratio(i[0],msg)>=60:
            print i[1]
            flag=1
            break
    if flag==0:
        print "Question Not found"
        

def structure(TXT):
    """
    This function adds given string (TXT) to the local dictionaries defined in the program
    In simpler words, makes given unstructured data to structured data
    """
    k=TXT.index('?')
    ans=TXT[k+1:]
    msg=(TXT[:k]).lower()
    tokens=nltk.word_tokenize(msg)
    for i in words:
        while (i in tokens):
            tokens.remove(i)
    txt=' '.join(tokens[1:])
    if tokens[0]=="who":
        lst=data_who
    elif tokens[0]=="what":
        lst=data_what
    elif tokens[0]=='how':
        lst=data_how
    lst.append(tuple([txt,ans]))    

