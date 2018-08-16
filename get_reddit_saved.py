import praw
import pandas as pd 
import datetime as dt 
from praw.models import Submission

reddit = praw.Reddit(client_id='XTJY4uWB8reLFA', 
client_secret='6Zl-Hm-u_SamDnjLRywz1BHx3WY', 
user_agent='Save_my_Saves', 
username='Terror_Rabbit', 
password='cApriItaly878')

saved = reddit.user.me().saved(limit=3)
thread_info_dict = {"title": [], "thumbnail": [] , "score": [], "subreddit": [], "permalink": [], "num_comments": []}

for item in saved:
    if isinstance(item, Submission):
        #permalink(gives you the reddit link), thumbnail, title , score, unsave
        thread_info_dict["title"].append(item.title)
        thread_info_dict["thumbnail"].append(item.thumbnail)
        thread_info_dict["subreddit"].append(item.subreddit)
        thread_info_dict["score"].append(item.score)
        thread_info_dict["permalink"].append(item.permalink)
        thread_info_dict["num_comments"].append(item.num_comments)
        print(item.title)
    else:
        #comments have no title or thumbnail
        thread_info_dict["title"].append(item.body)
        thread_info_dict["thumbnail"].append("Is Comment") 
        thread_info_dict["subreddit"].append(item.subreddit)
        thread_info_dict["score"].append(item.score)
        thread_info_dict["permalink"].append(item.permalink)
        thread_info_dict["num_comments"].append(item.num_comments)
        print(item.body, item.name, item.permalink, item.score, item.subreddit)
        
saved_data = pd.DataFrame(thread_info_dict, columns= thread_info_dict.keys())
saved_data.to_csv('reddit_saved.csv')