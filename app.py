import datetime
import os

import praw
import prawcore
from flask import Flask, url_for, render_template, request, flash, abort

app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # Get subreddit names from form.
        subreddit_names = str(request.form['subredditName'])

        # Perform input check.
        subreddit_names = check_input(subreddit_names=subreddit_names,
                                      template='submission.html')

        # Obtain a list with submissions to populate html page.
        subreddit_list = get_submissions(subreddit_names)

        if None in subreddit_list:
            # Display a warning to the user.
            flash('Something went wrong, check wheter input is correct.')
            return render_template('submissions.html')

        return render_template(template_name_or_list='submissions.html',
                               subreddit_list=subreddit_list,
                               get_date=get_date)


@app.route('/list', methods=['GET', 'POST'])
def list_subreddit():
    if request.method == 'GET':
        return render_template('list.html')
    else:
        # Get subreddit names from form.
        subreddit_names = request.form['subredditName']

        # Perform input check.
        subreddit_names = check_input(subreddit_names=subreddit_names,
                                      template='list.html')

        # Get time filter and number of submissions from form.
        time_filter = request.form['timeFilter']
        num_submission = request.form['numSubmission']

        # Perform input checks and get the submissions.
        time_filter_list = ['all', 'week', 'day', 'hour', 'month', 'week', 'year']
        if time_filter in time_filter_list and num_submission.isdigit():
            subreddit_list = get_submissions(subreddit_names=subreddit_names,
                                            time_filter=time_filter,
                                            num_submission=int(num_submission))
        elif time_filter in time_filter_list and num_submission.isdigit()==False:
            subreddit_list = get_submissions(subreddit_names=subreddit_names,
                                            time_filter=time_filter)
        elif time_filter not in time_filter_list and num_submission.isdigit():
            subreddit_list = get_submissions(subreddit_names=subreddit_names,
                                            num_submission=int(num_submission))
        else:
            subreddit_list = get_submissions(subreddit_names)

        if None in subreddit_list:
            # Display a warning to the user.
            flash('Something went wrong, check wheter input is correct.')
            return render_template('list.html')

        return render_template('submissions.html', subreddit_list=subreddit_list, get_date=get_date)

@app.route('/<string:subreddit>')
def list_subs(subreddit):
    """ Quick way to load page with given subreddit. """
    # Obtain a list to populate html page.
    subreddit_list = get_submissions(subreddit)

    return render_template('submissions.html', subreddit_list=subreddit_list, get_date=get_date)

@app.route('/<string:subreddit>/<int:num_submission>')
def list_subs_with_num(subreddit, num_submission):
    """ Quick way to load page with given subreddit and num_submissions. """
    # Obtain a list to populate html page.
    subreddit_list = get_submissions(subreddit_names=subreddit,
                                     num_submission=num_submission)

    return render_template('submissions.html', subreddit_list=subreddit_list, get_date=get_date)

########################################################################
#
# HELPER FUNCTIONS
#
########################################################################

def check_input(subreddit_names, template):
    """ Checks if user provided any subreddit name and split the input into
        list of subreddit names.
    Args:
        subreddit_names(str): String of user input.

        template(str): Template of .html page to render when user did not provide
            any subreddit names.

    Returns:
        List of separated subreddit names.
    """
    if subreddit_names != '':
        # Split every subreddit name into and remove whitespaces.
        subreddit_names = subreddit_names.split(',')
        for i, subreddit_name in enumerate(subreddit_names):
                subreddit_names[i] = subreddit_name.strip()

        return subreddit_names
    else:
        # Display a warning to the user if subreddit name was not provided.
        flash('Please provide subreddit name.')

        return render_template(template)

def get_submissions(subreddit_names, time_filter='day', num_submission=20):
    """
    Get list with reddit submissions from given subreddits using praw module.

    Args:
        subreddit_names (str, list): Subreddit name.

        time_filter (str): Type to sort top posts, e.g.: all, day, hour, month, week or year.

        submission_num: Number of submissions to scrap from reddit, e.g.: 10.

    Returns:
        List of tuples containing subreddit instance and submissions.
    """
    def download_submissions(subreddit_name):
        # Obtain Subreddit Instance.
        try:
            subreddit = reddit.subreddit(subreddit_name)
        except:
            # Returns None if provided subreddit name is incorrect.
            return None

        # Check early if subreddit exists or has any submissions.
        try:
            subreddit.top('day', limit=1).next()
        except:
            return None

        # Get top posts from Subreddit Instance.
        submissions = subreddit.top(time_filter, limit=num_submission)

        # Create tuple with subreddit instance and submissions.
        reddit_tuple = (subreddit_name, submissions)
        return reddit_tuple

    # Obtain Reddit Instance.
    reddit = praw.Reddit(client_id=os.environ.get('REDDIT_ID'),
                     client_secret=os.environ.get('REDDIT_SECRET'),
                     user_agent=os.environ.get('REDDIT_SECRET'))

    # Create an empty list to store subreddit instance and submissions.
    subreddit_list = []

    # Download submissions.
    if isinstance(subreddit_names, list):
        for subreddit_name in subreddit_names:
            subreddit_list.append(download_submissions(subreddit_name))

    elif isinstance(subreddit_names, str):
        subreddit_list.append(download_submissions(subreddit_names))

    else:
        raise TypeError("Input must be a string or a list.")

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
