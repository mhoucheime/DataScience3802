from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import string
from collections import Counter
 

punctuation = list(string.punctuation)
stopset = stopwords.words('english') + punctuation + ['amp','rt', 'via','trump','hillary','donald','clinton']

dictionary={"trump":{"don't": -1, "like": 1, "accuser": -1, "supporters": 1, "assault": -1, "believe": 1, "never": -1,  "sexual": -1, "can't": -1,  "accusers":-1, "drug": -1}, 
"clinton":{"emails": -1, "wikileaks": -1,  "fbi": -1, "like": -1, "rigged": -1 , "jail" : -1, "hacked" : -1,  "@wikileaks": -1, "drug":-1, "prosecuted": -1,  "rape": -1}}
 
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
    tokens = [token.lower() for token in tokens]    
    tokens = [token if not ("trump" in token or "hillary" in token or "donald" in token or "clinton" in token ) else '.' for token in tokens]
    
    if lowercase:
       tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
       
    return tokens


def parse(text, filename):
    tokens=preprocess(str(text))
    tokens = [w for w in tokens if not w in stopset]
    count_all = Counter()
    count_all.update(tokens)
    ## dev Note :  this is commented since we got the top 10 sentiment words
	##print filename+":"+ str(count_all.most_common(100))
	
	## calculating the sentiment values
	
    sentiment_words_dic = dictionary[filename]
	
    sentiment_words =[]
    for sentiment in sentiment_words_dic:
	sentiment_words.append(sentiment)
	
    total_sentiment = 0
    for token in tokens:
	if token in sentiment_words:
	   total_sentiment = total_sentiment + sentiment_words_dic[token]	
    print ("the sentiment of "+filename + " :"+str(total_sentiment))
	


with open('data/trump.txt', 'r') as text_file:
    text = text_file.read()
    parse(text,'trump')

with open('data/clinton.txt', 'r') as text_file:
    text = text_file.read()
    parse(text,'clinton')	
	
	
	
