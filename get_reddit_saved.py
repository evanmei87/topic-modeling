
# praw to get reddit threads
import praw
import pandas as pd 
from praw.models import Submission
import re
from math import log

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
words = open("words-by-frequency.txt").read().split()
wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)

def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))

# Log into reddit using praw
reddit = praw.Reddit(client_id='XTJY4uWB8reLFA', 
client_secret='6Zl-Hm-u_SamDnjLRywz1BHx3WY', 
user_agent='Save_my_Saves', 
username='Terror_Rabbit', 
password='cApriItaly878')

saved = reddit.user.me().saved(limit=3)
# Create a dictionary to store the thread's information
thread_info_dict = {"title": [], "body": [], "thumbnail": [] , "score": [], "subreddit": [], "permalink": [], "num_comments": [], "combined_text": []}

for item in saved:
    if isinstance(item, Submission):
        title = item.title
        body = item.selftext
        subreddit = re.sub(r"(\w)([A-Z])", r"\1 \2", infer_spaces(str(item.subreddit).lower()))

        thread_info_dict["title"].append(title)
        thread_info_dict["body"].append(body)
        thread_info_dict["thumbnail"].append(item.thumbnail)
        thread_info_dict["subreddit"].append(item.subreddit)
        thread_info_dict["score"].append(item.score)
        thread_info_dict["permalink"].append(item.permalink)
        thread_info_dict["num_comments"].append(item.num_comments)
        thread_info_dict["combined_text"].append(subreddit + " " + subreddit + " " + title + " " + body)
    else: # Is a saved comment
        submission = item.submission
        
        title = submission.title
        body = item.body
        subreddit = re.sub(r"(\w)([A-Z])", r"\1 \2", infer_spaces(str(item.subreddit).lower()))

        thread_info_dict["title"].append(title)
        thread_info_dict["body"].append(body)
        thread_info_dict["thumbnail"].append("Is Comment") 
        thread_info_dict["subreddit"].append(item.subreddit)
        thread_info_dict["score"].append(item.score)
        thread_info_dict["permalink"].append(item.permalink)
        thread_info_dict["num_comments"].append(item.num_comments) 
        thread_info_dict["combined_text"].append(subreddit + " " + subreddit + " " + title + " " + body)
        
saved_data = pd.DataFrame(thread_info_dict, columns= thread_info_dict.keys())
saved_data.to_csv('dataset.csv')