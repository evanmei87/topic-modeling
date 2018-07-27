import praw
import pandas as pd 
import datetime as dt 
from praw.models import Submission

reddit = praw.Reddit(client_id='XTJY4uWB8reLFA', 
client_secret='6Zl-Hm-u_SamDnjLRywz1BHx3WY', 
user_agent='Save_my_Saves', 
username='Terror_Rabbit', 
password='cApriItaly878')

saved = reddit.user.me().saved(limit=None)

for item in saved:
    if isinstance(item, Submission):
        print(item.title. item.id)
        