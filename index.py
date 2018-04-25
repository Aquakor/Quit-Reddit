from __future__ import unicode_literals
import urllib.request
import os
import sys
import datetime

import praw
import config
from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/')
def index():
    # Declare variables to get submissions from Reddit.
    subreddit_names = ['youtubehaiku', 'videos',
                       'mealtimevideos', 'livestreamfail',
                       'fortnitebr']
    time_filter = 'day'
    num_submission = 5

    # Obtain a list to populate html page.
    subreddit_list = get_submissions(subreddit_names, time_filter, num_submission)

    # Create html page with subreddit_list and get_date function.
    return render_template('index.html', subreddit_list=subreddit_list, get_date=get_date)


def get_submissions(subreddit_names, time_filter, num_submission):
    """
    Get list with reddit submissions from given
    list of subreddits using praw module.

    Args:
        subreddit_names (list): Subreddits names, e.g. ['youtubehaiku', 'videos'].

        time_filter (str): Type to sort top posts, e.g.: all, day, hour, month, week, year.

        submission_num: Number of submissions to scrap from reddit, e.g.: 10.

    Returns:
        List of tuples containing subreddit instance and submissions.
    """

    # Obtain Reddit Instance.
    reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent)

    # Create an empty list to store subreddit instance and submissions.
    subreddit_list = []

    for subreddit_name in subreddit_names:

        # Obtain Subreddit Instance.
        subreddit = reddit.subreddit(subreddit_name)

        # Get top posts from Subreddit Instance.
        submissions = subreddit.top(time_filter, limit=num_submission)

        # Create tuple with subreddit instance and submissions and append
        # the list to return.
        reddit_tuple = (subreddit, submissions)
        subreddit_list.append(reddit_tuple)

    return subreddit_list

def get_date(submission):
    """ Get date of a submission.
    Taken from: https://www.reddit.com/r/learnprogramming/comments/37kr5n/praw_is_it_possible_to_get_post_time_and_date/crphh68/.

    Args:
        Praw submission.

    Returns:
        Date of when the submission was created.
    """
    time = submission.created
    return datetime.datetime.fromtimestamp(time)
