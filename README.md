# DataScience3802
This repository contains all the projects and materials needed for Course Interdisciplinary 3802:Data Science Analysis w/Python-S 12:00 PM FALL 2016


###How to Run the Program and code

1. First run the twittering.py 
   
   ``` python 
    python tweetering.py clinton 1000 clinton.txt 
    ```

    This will create 1000 clinton tweets to data/clinton.txt 

   Do the same for Trump.

2. Then Run sentiment.py
   
   ``` python
   python sentiment.py
   ```
    
   This will save the sentiment for clinton and Trump in the data/output.txt


##Assumptions:
We take the top 10 associated sentiment words and discarded the neutral words like campaign,vote, gop , president , etc 



