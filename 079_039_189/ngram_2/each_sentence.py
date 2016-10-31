"""
Sanjay Reddy S-2013A7PS189P
Aditya Sarma  -2013A7PS079P
Vamsi T       -2013A7PS039P

Artificial Intelligence Term Project
"""


WEIGHT_FACTOR = 2.2

def convert_BSoup__to_text(soup):
    """
    THis function converts the BeautifulSoup object into string using a generator
    """
    return ''.join([str(x) for x in soup.findAll(text=True)])

def ignore_words(txt):
    """
    The results from google search have redundant words in them (happens when a crawler is extracting info).
    We found this while testing and went to search online and found it.
    One reference: https://productforums.google.com/forum/#!topic/webmasters/u2qsnn9TFiA
    The parameter txt is modified in the function
    """
    redundant_words = [ "Similar","Cached"] #Task: some more must be added
    for temp in redundant_words:
        txt = txt.replace(temp, "")
    return txt

def sentences(summary):
    """
    This function returns a list of sentences from BeautifulSoup object using other helper functions
    
    """
    txt = ignore_words(convert_BSoup__to_text(summary))
    sentences=[]
    for temp in txt.split("."): #splitting each sentence
        if temp:
            sentences.append(temp)
    lst = [re.sub(r"[^a-zA-Z ]", "", temp) for temp in sentences] #few special characters ('.','!',0-9) are removed from sentences
    return lst

def ngrams(lst, n=1):
    """
    Gives all possible n-grams (by defalut 1) from the list of words (lst).
    We can use nltk's in-buit n-gram function also. It returns a list of tuples
    """
    res=[]
    for i in xrange(len(lst)-n+1):
        res.apppend(tuple(lst[i:i+n]))
    return res    
    
def ngram_weight(ngram, marks):
    """
    This function returns the weight associated with the ngram parameter.
    This helps in the proper nouns being favoured as results (Since majority of 'Who' functions deal with them)
    """
    num = 0 #holds number of words starting with capitals
    for temp in ngram:
        if temp == temp.capitalize():
            num+=1 
    return marks * (WEIGHT_FACTOR**num)


    
