"""
Sanjay Reddy S-2013A7PS189P
Aditya Sarma  -2013A7PS079P
Vamsi T       -2013A7PS039P

Artificial Intelligence Term Project
"""


import pickle
import BeautifulSoup
import re
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from google import search


def get_10_summary(query, source="google"):
    """
    This function returns the first ten (or less, if 10 are not present) summaries when the query (a string) is run on the source (here google).
    The return type is a beautifulSoup module's object and is similar to a list
    """
    
    result = search(query) #calls query on google
    #print "---------------------------" + str(type(results)) + "---------------------------"
    return result

