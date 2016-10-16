from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import string
from collections import Counter
 

''' Our Stop words contain the nltk stop words, punctuation and some names like clinton , hillary , etc''' 
punctuation = list(string.punctuation)
stopset = stopwords.words('english') + punctuation + ['amp','rt', 'via','trump','hillary','donald','clinton']


''' Top 10 Sentiment words for Trump and Clinton which we store in key value kind of dictionary  '''
dictionary={"trump":{"don't": -1, "like": 1, "accuser": -1, "supporters": 1, "assault": -1, "believe": 1, "never": -1,  "sexual": -1, "can't": -1,  "accusers":-1, "drug": -1}, 
"clinton":{"emails": -1, "wikileaks": -1,  "fbi": -1, "like": -1, "rigged": -1 , "jail" : -1, "hacked" : -1,  "@wikileaks": -1, "drug":-1, "prosecuted": -1,  "rape": -1}}
 

'''Removing the emoticons '''

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
url_re = re.compile('(.*?)http.*?\s?(.*?)',re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
	## Making all words into lower case
    tokens = [token.lower() for token in tokens]    
    ### removing the words like trump , hillary , clinton
    tokens = [token if not ("trump" in token or "hillary" in token or "donald" in token or "clinton" in token ) else '.' for token in tokens]
    
    if lowercase:
       tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
       
    return tokens


def parse(text, filename,file):
    tokens=preprocess(str(text))
    ## removing all the stop words
    tokens = [w for w in tokens if not w in stopset]
    
    ## creating a counter to count the frequency of words
    count_all = Counter()
    count_all.update(tokens)
    ## dev Note :  this is commented since we got the top 10 sentiment words
    ##print filename+":"+ str(count_all.most_common(100))
	
    ## getting the sentiment words for trump or clinton
    sentiment_words_dic = dictionary[filename]
	
    sentiment_words =[]
    for sentiment in sentiment_words_dic:
	sentiment_words.append(sentiment)
	
    ## calculating the sentiment values
    total_sentiment = 0
    for token in tokens:
	if token in sentiment_words:
	   total_sentiment = total_sentiment + sentiment_words_dic[token]	
    print ("the sentiment of "+filename + " :"+str(total_sentiment))
	
    
    file.write("the sentiment of "+filename + " :"+str(total_sentiment))
    
	
	
'''This is where the program starts'''
file =  open("data/output.txt", 'w')	
## reading the Trump tweets file	
with open('data/trump.txt', 'r') as text_file:
    text = text_file.read()
    parse(text,'trump', file)

file.write("\n")

## reading the clinton tweets
with open('data/clinton.txt', 'r') as text_file:
    text = text_file.read()
    parse(text,'clinton',file)	
	
file.close()	
	
